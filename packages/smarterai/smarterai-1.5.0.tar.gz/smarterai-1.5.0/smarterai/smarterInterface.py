import inspect
import logging
from typing import Optional
from abc import ABCMeta, abstractmethod
from smarterai.smarterApi import SmarterMessage, SmarterSender, SmarterApi

logger = logging.getLogger("__SMARTER_INTERFACE__")
logger.setLevel(level=logging.WARNING)


class _Smarter_SignatureCheckerMeta(ABCMeta):
    def __init__(cls, name, bases, attrs):
        signature_errors = []
        for base_class in bases:
            for func_name in getattr(base_class, "__abstractmethods__", ()):
                smarter_signature = inspect.getfullargspec(
                    getattr(base_class, func_name)
                )
                flex_signature = inspect.getfullargspec(
                    getattr(cls, func_name)
                )
                if base_class.__name__ == 'SmarterPlugin':
                    if func_name == 'invoke':
                        warning_text = 'SmarterPlugin Class has been deprecated. Use ' \
                                       'SmarterApp and SmarterApp.invoke(self, port: str, message: SmarterMessage, ' \
                                       'smarter_api: SmarterApi)->Optional[SmarterMessage]: instead'
                    else:
                        warning_text = 'SmarterPlugin Class has been deprecated. Use SmarterApp instead'
                    logger.warning(DeprecationWarning(warning_text))
                if smarter_signature != flex_signature:
                    signature_errors.append(
                        f"Abstract method {func_name} "
                        f"not implemented with correct signature in {cls.__name__}. Expected {smarter_signature}."
                    )

        if signature_errors:
            raise TypeError("\n".join(signature_errors))
        super().__init__(name, bases, attrs)


class SmarterApp(metaclass=_Smarter_SignatureCheckerMeta):
    """
    SmarterPlugin is designed for easy communication between the smarter.ai's platform and other Flex.
    In order to have the Flex's code accessible to the platform, this class needs to be inherited from
    a class explicitly named SmarterComponent.
    Example:
        Class SmarterComponent(SmarterPlugin):
            pass
    """

    @abstractmethod
    def invoke(
            self, port: str, message: SmarterMessage, smarter_api: SmarterApi
    ) -> Optional[SmarterMessage]:
        """
        This is the flex's messages entry point. Any message sent to the current flex will be routed to this method.
        This method needs to be overwritten.

        Example:
            Class SmarterComponent(SmarterPlugin):
                def invoke(self, port: str,
                           msg: SmarterMessage,
                           smarter_api: SmarterApi) -> Optional[SmarterMessage]:
                    pass
        The message received and its associated port will be passed as inputs for this method,
        Along with a callable function that can be used to send messages to other flex.

        Arguments:
            port [str]: The input port name used to receive the message.
            msg [SmarterMessage]: The message passed to the flex.
            smarter_api[SmarterApi]: A Callable function used to send messages to other flex.
                                    The function has the signature:
                                        Callable[[SmarterMessage, str], SmarterMessage]
                                    Example:
                                        send_message(SmarterMessage(), 'out_port_name')

                                    Arguments:
                                        [SmarterMessage]: The new message to send out.
                                        [str]: The output port name used to send the new message.

                                    Returns:
                                        [SmarterMessage]: A return message.

        Returns:
            Optional[SmarterMessage]: If a message is being returned it should be of
                                      type SmarterMessage or None
        """
        raise NotImplementedError


class SmarterPlugin(metaclass=_Smarter_SignatureCheckerMeta):
    """
    SmarterPlugin is designed for easy communication between the smarter.ai's platform and other Flex.
    In order to have the Flex's code accessible to the platform, this class needs to be inherited from
    a class explicitly named SmarterComponent.
    Example:
        Class SmarterComponent(SmarterPlugin):
            pass
    """

    @abstractmethod
    def invoke(
            self, port: str, message: SmarterMessage, sender: SmarterSender
    ) -> Optional[SmarterMessage]:
        """
        This is the flex's messages entry point. Any message sent to the current flex will be routed to this method.
        This method needs to be overwritten.

        Example:
            Class SmarterComponent(SmarterPlugin):
                def invoke(self, port: str,
                           msg: SmarterMessage,
                           send_message: SmarterSender) -> Optional[SmarterMessage]:
                    pass
        The message received and its associated port will be passed as inputs for this method,
        Along with a callable function that can be used to send messages to other flex.

        Arguments:
            port [str]: The input port name used to receive the message.
            msg [SmarterMessage]: The message passed to the flex.
            send_message[SmarterSender]: A Callable function used to send messages to other flex.
                                        The function has the signature:
                                            Callable[[SmarterMessage, str], SmarterMessage]
                                        Example:
                                            send_message(SmarterMessage(), 'out_port_name')

                                        Arguments:
                                            [SmarterMessage]: The new message to send out.
                                            [str]: The output port name used to send the new message.

                                        Returns:
                                            [SmarterMessage]: A return message.

        Returns:
            Optional[SmarterMessage]: If a message is being returned it should be of
                                      type SmarterMessage or None
        """
        raise NotImplementedError
