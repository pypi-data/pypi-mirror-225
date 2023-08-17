#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

from __future__ import print_function

import time

import ibm_watson_machine_learning._wrappers.requests as requests
from ibm_watson_machine_learning.messages.messages import Messages
from ibm_watson_machine_learning.utils import INSTANCE_DETAILS_TYPE
from ibm_watson_machine_learning import APIClient
from ibm_watson_machine_learning.wml_client_error import WMLClientError
from ibm_watson_machine_learning.wml_resource import WMLResource
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes, DecodingMethods
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames, GenTextReturnOptMetaNames


_DEFAULT_LIST_LENGTH = 50


class Model(WMLResource):
    """Instantiate the model interface.

    :param model_id: the type of model to use
    :type model_id: str

    :param credentials: credentials to Watson Machine Learning instance
    :type credentials: dict

    :param params: parameters to use during generate requests
    :type params: dict, optional

    :param project_id: ID of the Watson Studio project
    :type project_id: str, optional

    :param space_id: ID of the Watson Studio space
    :type space_id: str, optional

    :param verify: user can pass as verify one of following:

        - the path to a CA_BUNDLE file
        - the path of directory with certificates of trusted CAs
        - `True` - default path to truststore will be taken
        - `False` - no verification will be made
    :type verify: bool or str, optional

    **Example**

    .. code-block:: python

        from ibm_watson_machine_learning.foundation_models import Model
        from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
        from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes, DecodingMethods

        # To display example params enter
        GenParams().get_example_values()

        generate_params = {
            GenParams.MAX_NEW_TOKENS: 25
        }

        model = Model(
            model_id=ModelTypes.FLAN_UL2,
            params=generate_params,
            credentials={
                "apikey": "***",
                "url": "https://us-south.ml.cloud.ibm.com"
            },
            project_id="*****"
            )
    """

    def __init__(self,
                 model_id: str,
                 credentials: dict,
                 params: dict = None,
                 project_id: str = None,
                 space_id: str = None,
                 verify = None) -> None:

        self.model_id = model_id
        if isinstance(self.model_id, ModelTypes):
            self.model_id = self.model_id.value
        self.params = params
        self.project_id = project_id
        self.space_id = space_id
        self._client = APIClient(credentials, verify=verify)

        Model._validate_type(params, u'params', dict, False)

        if not self._client.CLOUD_PLATFORM_SPACES:
            raise WMLClientError.__init__(self, f"Operation is unsupported for this release.")

        if space_id:
            self._client.set.default_space(space_id)
        else:
            self._client.set.default_project(project_id)

        WMLResource.__init__(self, __name__, self._client)

    def get_details(self):
        """Get model's details

        :return: model's details
        :rtype: dict

        **Example**

        .. code-block:: python

            model.get_details()

        """
        limit = 200
        asynchronous = False
        get_all = False

        url = self._client.service_instance._href_definitions.get_fm_specifications_href(limit)
        models = self._get_artifact_details(base_url=url, uid=None, limit=limit, resource_name='foundation_models', _async=asynchronous, _all=get_all)['resources']

        return next((item for item in models if item['model_id'] == self.model_id), None)

    def generate(self, prompt, params=None):
        """Given a text prompt as input, and parameters the selected model (model_id)
        will generate a completion text as generated_text.

        :param params: meta props for text generation, use ``ibm_watson_machine_learning.metanames.GenTextParamsMetaNames().show()`` to view the list of MetaNames
        :type params: dict

        :param prompt: the prompt string
        :type prompt: str

        :return: scoring result containing generated content
        :rtype: dict

        **Example**

        .. code-block:: python

            q = "What is 1 + 1?"
            generated_response = model.generate(prompt=q)
            print(generated_response['results'][0]['generated_text'])

        """
        generate_text_url = self._client.service_instance._href_definitions.get_fm_generation_href('text?version=2022-08-01')
        Model._validate_type(params, u'params', dict, False)
        Model._validate_type(prompt, u'prompt', str, True)
        payload = {
            "model_id": self.model_id,
            "input": prompt,
        }

        if params:
            payload['parameters'] = params
        elif self.params:
            payload['parameters'] = self.params

        if 'parameters' in payload and GenTextParamsMetaNames.DECODING_METHOD in payload['parameters']:
            if isinstance(payload['parameters'][GenTextParamsMetaNames.DECODING_METHOD], DecodingMethods):
                payload['parameters'][GenTextParamsMetaNames.DECODING_METHOD] = payload['parameters'][GenTextParamsMetaNames.DECODING_METHOD].value

        if self._client.default_project_id:
            payload['project_id'] = self._client.default_project_id
        elif self._client.default_space_id:
            payload['space_id'] = self._client.default_space_id

        if 'parameters' in payload and 'return_options' in payload['parameters']:
            if not (payload['parameters']['return_options'].get("input_text", False) or payload['parameters']['return_options'].get("input_tokens", False)):
                raise WMLClientError(Messages.get_message(message_id="fm_required_parameters_not_provided"))

        retries = 0
        while retries < 3:
            response_scoring = requests.post(
                url=generate_text_url,
                json=payload,
                headers=self._client._get_headers())
            if response_scoring.status_code == 429 and 'user_rate_limit_reached' in response_scoring.text:
                time.sleep(2 ** retries)
                retries += 1
            else:
                break

        return self._handle_response(200, u'generate', response_scoring)

    def generate_text(self, prompt, params=None):
        """Given a text prompt as input, and parameters the selected model (model_id)
        will generate a completion text as generated_text.

        :param params: meta props for text generation, use ``ibm_watson_machine_learning.metanames.GenTextParamsMetaNames().show()`` to view the list of MetaNames
        :type params: dict

        :param prompt: the prompt string
        :type prompt: str

        :return: generated content
        :rtype: str

        **Example**

        .. code-block:: python

            q = "What is 1 + 1?"
            generated_text = model.generate_text(prompt=q)
            print(generated_text)

        """
        return self.generate(prompt=prompt, params=params)['results'][0]['generated_text']
