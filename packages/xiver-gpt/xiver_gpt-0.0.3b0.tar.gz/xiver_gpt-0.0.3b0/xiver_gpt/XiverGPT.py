from typing import Any, Generator
import inspect

import g4f

from .exceptions import NoProvider

__all__ = ("XiverGPT",)


PROVIDERS_BLACKLIST = (
    g4f.Provider.Providers.DfeHub,
    g4f.Provider.Providers.Ails,
    g4f.Provider.Providers.Bard,
)


class XiverGPT:
    """The main class of xiver_gpt lib
    """
    def __init__(self, *, g4f_model: g4f.Model.model = g4f.Model.gpt_4, \
                 g4f_provider: Any | None = None, \
                 stream: bool = False) -> None:

        self.g4f_worked_providers = []

        # Support vars
        self.__provider_num = 0

        self.g4f_model      = g4f_model
        self.g4f_provider   = g4f_provider

        self.stream = stream

        self.providers  = [cls_obj for _, cls_obj in inspect.getmembers(g4f.Provider) if inspect.ismodule(cls_obj)]
        self.models     = [cls_obj for _, cls_obj in inspect.getmembers(g4f.Model) if inspect.isclass(cls_obj)]

        try:
            self.models.remove(type)
            self.providers.remove(type)
        except ValueError:
            pass

        self.providers.remove(g4f.Provider.Provider)
        self.providers.remove(g4f.Provider.Providers)
        self.models.remove(g4f.Model.model)

        self.auto_update_provider()

    def auto_update_provider(self) -> None:  # pylint: disable=too-many-branches
        if self.g4f_provider:
            try:
                response = g4f.ChatCompletion.create(model=self.g4f_model, provider=self.g4f_provider, messages=[
                                            {"role": "user", "content": "Hello world"}], stream=self.stream)

                if 'is not working' in response or \
                        'error' in response or \
                        not response:
                    raise
            except Exception as exc:
                raise NoProvider(self.g4f_model) from exc

            self.g4f_worked_providers.append(self.g4f_provider)
            return

        work_providers = []
        for provider in self.providers:

            if not provider.working or provider.supports_stream < self.stream or \
                provider in PROVIDERS_BLACKLIST:
                continue

            try:
                response = g4f.ChatCompletion.create(model=self.g4f_model, provider=provider, messages=[
                                            {"role": "user", "content": "Hello world"}], stream=self.stream)

                res = response if not self.stream else ' '.join([i for i in response])

                if 'is not working' in res or \
                    'error' in res or \
                        not res:
                    raise
                work_providers.append(provider)
            except:  # pylint: disable=bare-except
                pass

        for prov in work_providers:
            response = g4f.ChatCompletion.create(model=self.g4f_model, provider=prov, messages=[
                                    {"role": "user", "content": "Hello world"}], stream=self.stream)
            res = ''
            for i in response:
                res.join(i)

            if 'error' not in res:
                self.g4f_worked_providers.append(prov)

        if not self.g4f_worked_providers:
            raise NoProvider(self.g4f_model)

    def create_response(self, message: str, stream: bool = False) -> str | Generator:
        response = g4f.ChatCompletion.create(
            model=self.g4f_model,
            provider=self.g4f_worked_providers[self.__provider_num],
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ],
            stream=stream,
        )

        while not response:
            self.__provider_num += 1
            if self.__provider_num > len(self.g4f_worked_providers):
                self.__provider_num = 0

            response = g4f.ChatCompletion.create(
                model=self.g4f_model,
                provider=self.g4f_worked_providers[self.__provider_num],
                messages=[
                    {
                        "role": "user",
                        "content": message,
                    }
                ],
                stream=stream,
            )
        
        return response
