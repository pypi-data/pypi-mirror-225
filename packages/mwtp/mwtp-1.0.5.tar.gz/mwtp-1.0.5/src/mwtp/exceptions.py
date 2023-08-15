class InvalidTitle(Exception):
	'''
	Umbrella exception for all kinds of exceptions
	a parser might raise.
	'''
	pass


class TitleContainsIllegalCharacter(InvalidTitle):
	
	def __init__(self) -> None:
		super().__init__('Title contains illegal characters')


class TitleContainsSignatureComponent(InvalidTitle):
	
	def __init__(self) -> None:
		super().__init__('Title contains a signature component')


class TitleContainsURLEncodedCharacter(InvalidTitle):
	
	def __init__(self) -> None:
		super().__init__('Title contains a URL-encoded character')


class TitleContainsHTMLEntity(InvalidTitle):
	
	def __init__(self) -> None:
		super().__init__('Title contains a HTML entity look-alike')


class TitleHasRelativePathComponent(InvalidTitle):
	
	def __init__(self) -> None:
		super().__init__('Title contains a relative path component')


class TitleHasSecondLevelNamespace(InvalidTitle):
	
	def __init__(self) -> None:
		super().__init__('Second level namespace cannot be resolved')


class TitleIsBlank(InvalidTitle):
	
	def __init__(self) -> None:
		super().__init__('Title is blank or only has the namespace part')


class TitleIsTooLong(InvalidTitle):
	
	def __init__(self) -> None:
		super().__init__('Title exceeds maximum length of 256 bytes')


class TitleStartsWithColon(InvalidTitle):
	
	def __init__(self) -> None:
		super().__init__('Invalid colon at the start of namespace or page name')
