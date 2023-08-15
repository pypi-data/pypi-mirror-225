

NoOneButtonParamIsFilled = ValueError("No one button parameters is filled")

DifferentButtonsInMatrix = ValueError("Only one type of button is allowed in the markup")

UnknownButtonType = ValueError("UnknownButtonType")

TooMoreCharacters = ValueError(
    "The callback data can be only 64 bytes"
    "(~62 or less characters because separator)"
)

RecursionObjectParse = ValueError("Now objects cannot contain objects")

WrongObjectType = ValueError("Wrong object type in the decode")

CantEditMedia = ValueError("Error for edit message media")

BotIsUndefined = ValueError("Bot is not defined in StakerMiddleware")

MessageTooOld = ValueError("Message too old and has not message param")

MessageTextIsNone = ValueError("Message text is None")

UndefinedMagicFilterModel = ValueError("Magic filter model is undefined")

UndefinedType = ValueError("Error event type in a middleware")

CallbackEventWasNotGiven = ValueError("Callback event was not given to decoder")


class Throttling(Exception):
    def __init__(self):
        self.message = "User got trottling exception"

        super().__init__(self.message)

