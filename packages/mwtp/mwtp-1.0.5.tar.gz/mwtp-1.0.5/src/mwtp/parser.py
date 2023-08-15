import re

from ._alias_record import AliasRecord
from ._dcs import Namespace, NamespaceData
from ._namespace_id_map import NamespaceIDMap
from ._php_to_upper_map import PHP_TO_UPPER_MAP
from ._title_like import TitleLike
from .exceptions import (
	TitleContainsHTMLEntity,
	TitleContainsIllegalCharacter,
	TitleContainsSignatureComponent,
	TitleContainsURLEncodedCharacter,
	TitleHasRelativePathComponent,
	TitleHasSecondLevelNamespace,
	TitleIsBlank,
	TitleIsTooLong,
	TitleStartsWithColon
)
from .title import Title


class Parser:
	
	__slots__ = ('_namespace_data', '_namespace_id_map')
	
	_TITLE_MAX_BYTES = 255
	_ILLEGAL_TITLE_CHARACTER = re.compile(
		r'''[\u0000-\u001F#<>[\]{|}\u007F\uFFFD]'''
	)
	_TO_UPPER_MAP = PHP_TO_UPPER_MAP
	
	def __init__(self, namespace_data, alias_entries):
		self._namespace_data = {}
		self._namespace_id_map = NamespaceIDMap()
		
		alias_record = AliasRecord(alias_entries)
		
		self._initialize_data_record(namespace_data, alias_record)
		self._initialize_namespace_map()
	
	def _initialize_data_record(self, namespace_data, alias_record):
		for namespace_id, entry in namespace_data.items():
			arguments = {**entry}
			aliases = alias_record[namespace_id]
			
			if aliases:
				arguments['aliases'] = aliases
			
			self._namespace_data[namespace_id] = NamespaceData(**arguments)
	
	def _initialize_namespace_map(self):
		for namespace in self._namespace_data.values():
			keys_to_be_added = [namespace.name]
			keys_to_be_added.extend(namespace.aliases)
			
			if namespace.canonical:
				keys_to_be_added.append(namespace.canonical)
			
			for key in keys_to_be_added:
				self._namespace_id_map[key] = namespace.id
	
	@property
	def namespace_data(self):
		return self._namespace_data
	
	def parse(self, string):
		title_like = TitleLike(string)
		title_like.sanitize()
		
		if title_like.starts_with(':'):
			title_like.extract(1)
		
		title_like.remove_fragment_if_any()
		
		namespace, page_name = self._split_title(title_like)
		
		self._validate_characters(page_name)
		self._validate_page_name_length(TitleLike(page_name), namespace)
		
		return self._make_title(page_name, namespace)
	
	def _make_title(self, page_name, namespace):
		corresponding_namespace_data = self._namespace_data[str(namespace)]
		casing_rule = corresponding_namespace_data.case
		cased_page_name = self._apply_casing_rule(page_name, casing_rule)
		
		return Title(
			name = cased_page_name,
			namespace = namespace,
			parser = self
		)
	
	@staticmethod
	def _apply_casing_rule(page_name, casing_rule):
		if casing_rule == 'case-sensitive':
			cased_page_name = page_name
		
		elif casing_rule == 'first-letter':
			first_character, the_rest = page_name[0], page_name[1:]
			first_character_code = ord(first_character)
			
			if first_character_code not in PHP_TO_UPPER_MAP:
				uppercased_first_char = first_character.upper()
			else:
				uppercased_first_char = \
					first_character.translate(PHP_TO_UPPER_MAP)
			
			cased_page_name = uppercased_first_char + the_rest
		
		else:
			raise TypeError(f'Case rule unrecognized: {casing_rule}')
		
		return cased_page_name
	
	def _split_title(self, title_like):
		if title_like.starts_with(':'):
			raise TitleStartsWithColon
		
		namespace, page_name = title_like.split_by_first_colon()
		namespace_id = self._namespace_id_map[namespace]
		
		if page_name == '':
			raise TitleIsBlank
		
		if page_name.startswith(':'):
			raise TitleStartsWithColon
		
		if namespace is None or namespace_id is None:
			return Namespace.MAIN, page_name
		
		if namespace_id != Namespace.TALK or ':' not in page_name:
			return namespace_id, page_name
		
		self._validate_second_level_namespace(page_name)
		
		return namespace_id, page_name
	
	def _validate_second_level_namespace(self, page_name):
		title_like = TitleLike(page_name)
		second_level_namespace, _ = title_like.split_by_first_colon()
		
		if second_level_namespace in self._namespace_id_map:
			raise TitleHasSecondLevelNamespace
	
	def _validate_characters(self, page_name):
		title_like = TitleLike(page_name)
		
		if self._ILLEGAL_TITLE_CHARACTER.search(page_name):
			raise TitleContainsIllegalCharacter
		
		if title_like.contains_url_encoded_character():
			raise TitleContainsURLEncodedCharacter
		
		if title_like.contains_html_entity_like():
			raise TitleContainsHTMLEntity
		
		if title_like.has_relative_path_component():
			raise TitleHasRelativePathComponent
		
		if title_like.contains_signature_component():
			raise TitleContainsSignatureComponent
	
	def _validate_page_name_length(self, page_name, namespace):
		not_a_special_page = namespace != Namespace.SPECIAL
		exceeds_max_byte_length = len(page_name) > self._TITLE_MAX_BYTES
		
		if not_a_special_page and exceeds_max_byte_length:
			raise TitleIsTooLong
