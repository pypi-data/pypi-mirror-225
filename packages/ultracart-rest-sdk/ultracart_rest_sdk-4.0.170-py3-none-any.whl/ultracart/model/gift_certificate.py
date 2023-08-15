"""
    UltraCart Rest API V2

    UltraCart REST API Version 2  # noqa: E501

    The version of the OpenAPI document: 2.0.0
    Contact: support@ultracart.com
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

from ultracart.model_utils import (  # noqa: F401
    ApiTypeError,
    ModelComposed,
    ModelNormal,
    ModelSimple,
    cached_property,
    change_keys_js_to_python,
    convert_js_args_to_python_args,
    date,
    datetime,
    file_type,
    none_type,
    validate_get_composed_info,
    OpenApiModel
)
from ultracart.exceptions import ApiAttributeError


def lazy_import():
    from ultracart.model.gift_certificate_ledger_entry import GiftCertificateLedgerEntry
    globals()['GiftCertificateLedgerEntry'] = GiftCertificateLedgerEntry


class GiftCertificate(ModelNormal):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Attributes:
      allowed_values (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          with a capitalized key describing the allowed value and an allowed
          value. These dicts store the allowed enum values.
      attribute_map (dict): The key is attribute name
          and the value is json key in definition.
      discriminator_value_class_map (dict): A dict to go from the discriminator
          variable value to the discriminator class name.
      validations (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          that stores validations for max_length, min_length, max_items,
          min_items, exclusive_maximum, inclusive_maximum, exclusive_minimum,
          inclusive_minimum, and regex.
      additional_properties_type (tuple): A tuple of classes accepted
          as additional properties values.
    """

    allowed_values = {
    }

    validations = {
        ('email',): {
            'max_length': 100,
        },
    }

    @cached_property
    def additional_properties_type():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded
        """
        lazy_import()
        return (bool, date, datetime, dict, float, int, list, str, none_type,)  # noqa: E501

    _nullable = False

    @cached_property
    def openapi_types():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded

        Returns
            openapi_types (dict): The key is attribute name
                and the value is attribute type.
        """
        lazy_import()
        return {
            'activated': (bool,),  # noqa: E501
            'code': (str,),  # noqa: E501
            'customer_profile_oid': (int,),  # noqa: E501
            'deleted': (bool,),  # noqa: E501
            'email': (str,),  # noqa: E501
            'expiration_dts': (str,),  # noqa: E501
            'gift_certificate_oid': (int,),  # noqa: E501
            'internal': (bool,),  # noqa: E501
            'ledger_entries': ([GiftCertificateLedgerEntry],),  # noqa: E501
            'merchant_id': (str,),  # noqa: E501
            'merchant_note': (str,),  # noqa: E501
            'original_balance': (float,),  # noqa: E501
            'reference_order_id': (str,),  # noqa: E501
            'remaining_balance': (float,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'activated': 'activated',  # noqa: E501
        'code': 'code',  # noqa: E501
        'customer_profile_oid': 'customer_profile_oid',  # noqa: E501
        'deleted': 'deleted',  # noqa: E501
        'email': 'email',  # noqa: E501
        'expiration_dts': 'expiration_dts',  # noqa: E501
        'gift_certificate_oid': 'gift_certificate_oid',  # noqa: E501
        'internal': 'internal',  # noqa: E501
        'ledger_entries': 'ledger_entries',  # noqa: E501
        'merchant_id': 'merchant_id',  # noqa: E501
        'merchant_note': 'merchant_note',  # noqa: E501
        'original_balance': 'original_balance',  # noqa: E501
        'reference_order_id': 'reference_order_id',  # noqa: E501
        'remaining_balance': 'remaining_balance',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_openapi_data(cls, *args, **kwargs):  # noqa: E501
        """GiftCertificate - a model defined in OpenAPI

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            activated (bool): True if this gift certificate is activated and ready to apply to purchases.. [optional]  # noqa: E501
            code (str): The code used by the customer to purchase against this gift certificate.. [optional]  # noqa: E501
            customer_profile_oid (int): This is the customer profile oid associated with this internally managed gift certificate.. [optional]  # noqa: E501
            deleted (bool): True if this gift certificate was deleted.. [optional]  # noqa: E501
            email (str): Email of the customer associated with this gift certificate.. [optional]  # noqa: E501
            expiration_dts (str): Expiration date time.. [optional]  # noqa: E501
            gift_certificate_oid (int): Gift certificate oid.. [optional]  # noqa: E501
            internal (bool): This is an internally managed gift certificate associated with the loyalty cash rewards program.. [optional]  # noqa: E501
            ledger_entries ([GiftCertificateLedgerEntry]): A list of all ledger activity for this gift certificate.. [optional]  # noqa: E501
            merchant_id (str): Merchant Id. [optional]  # noqa: E501
            merchant_note (str): A list of all ledger activity for this gift certificate.. [optional]  # noqa: E501
            original_balance (float): Original balance of the gift certificate.. [optional]  # noqa: E501
            reference_order_id (str): The order used to purchase this gift certificate.  This value is ONLY set during checkout when a certificate is purchased, not when it is used.  Any usage is recorded in the ledger. [optional]  # noqa: E501
            remaining_balance (float): The remaining balance on the gift certificate.  This is never set directly, but calculated from the ledger.  To change the remaining balance, add a ledger entry.. [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', True)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        self = super(OpenApiModel, cls).__new__(cls)

        if args:
            for arg in args:
                if isinstance(arg, dict):
                    kwargs.update(arg)
                else:
                    raise ApiTypeError(
                        "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                            args,
                            self.__class__.__name__,
                        ),
                        path_to_item=_path_to_item,
                        valid_classes=(self.__class__,),
                    )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
        return self

    required_properties = set([
        '_data_store',
        '_check_type',
        '_spec_property_naming',
        '_path_to_item',
        '_configuration',
        '_visited_composed_classes',
    ])

    @convert_js_args_to_python_args
    def __init__(self, *args, **kwargs):  # noqa: E501
        """GiftCertificate - a model defined in OpenAPI

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            activated (bool): True if this gift certificate is activated and ready to apply to purchases.. [optional]  # noqa: E501
            code (str): The code used by the customer to purchase against this gift certificate.. [optional]  # noqa: E501
            customer_profile_oid (int): This is the customer profile oid associated with this internally managed gift certificate.. [optional]  # noqa: E501
            deleted (bool): True if this gift certificate was deleted.. [optional]  # noqa: E501
            email (str): Email of the customer associated with this gift certificate.. [optional]  # noqa: E501
            expiration_dts (str): Expiration date time.. [optional]  # noqa: E501
            gift_certificate_oid (int): Gift certificate oid.. [optional]  # noqa: E501
            internal (bool): This is an internally managed gift certificate associated with the loyalty cash rewards program.. [optional]  # noqa: E501
            ledger_entries ([GiftCertificateLedgerEntry]): A list of all ledger activity for this gift certificate.. [optional]  # noqa: E501
            merchant_id (str): Merchant Id. [optional]  # noqa: E501
            merchant_note (str): A list of all ledger activity for this gift certificate.. [optional]  # noqa: E501
            original_balance (float): Original balance of the gift certificate.. [optional]  # noqa: E501
            reference_order_id (str): The order used to purchase this gift certificate.  This value is ONLY set during checkout when a certificate is purchased, not when it is used.  Any usage is recorded in the ledger. [optional]  # noqa: E501
            remaining_balance (float): The remaining balance on the gift certificate.  This is never set directly, but calculated from the ledger.  To change the remaining balance, add a ledger entry.. [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        if args:
            for arg in args:
                if isinstance(arg, dict):
                    kwargs.update(arg)
                else:
                    raise ApiTypeError(
                        "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                            args,
                            self.__class__.__name__,
                        ),
                        path_to_item=_path_to_item,
                        valid_classes=(self.__class__,),
                    )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
            if var_name in self.read_only_vars:
                raise ApiAttributeError(f"`{var_name}` is a read-only attribute. Use `from_openapi_data` to instantiate "
                                     f"class with read only attributes.")
