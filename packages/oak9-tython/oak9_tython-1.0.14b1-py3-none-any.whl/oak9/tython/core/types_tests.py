import unittest
from typing import List

from core.proxyobjs import PathTrackerProxy

from parameterized import parameterized
from core.types import Finding, FindingType, Severity, RelatedConfig, WellDoneRating, Violation
from models.aws.aws_apigatewayv2_pb2 import *

class FindingTests(unittest.TestCase):
    related_config_1 = RelatedConfig()
    related_config_1.config_id = "bucket.lifecycle_configuration.rules[0].id"
    related_config_1.preferred_value = "VersioningLifecycleManagementRule"
    related_config_1.comment = "change name to a name for your rule"

    related_config_2 = RelatedConfig()
    related_config_2.config_id = "bucket.lifecycle_configuration.rules[0].status"
    related_config_2.preferred_value = "Enabled"

    related_configs = [related_config_1, related_config_2]

    @parameterized.expand(
        [
            [Finding(
                finding_type=FindingType.DesignGap,
                gap="S3 Lifecycle configuration is not defined",
                rating=Severity.Critical,
                desc="Define the appropriate lifecycle configuration",
                config_id='bucket.lifecycle_configuration',
                related_configs=related_configs),
                False,
                'Design Gap Finding w/ Related Configs - No Exceptions'
            ],
            [Finding(
                finding_type=FindingType.ResourceGap,
                gap="Dynamo DB tables are not globally available",
                rating=Severity.High,
                desc="Since your design preference is to have a globally available database, use DynamoDB Global tables instead",
                config_id='db'),
                False,
                'Resource Gap Finding - No Exceptions'
            ],
            [Finding(
                finding_type=FindingType.Kudos,
                config_id='key.algorithm',
                desc="Key algorithm is set to AES-GCM",
                rating=WellDoneRating.Amazing),
                False,
                'Well Done Finding - No Exceptions'
            ],
            [Finding(
                FindingType.Task,
                req_id='Oak9.Req.KM.1',
                desc="Ensure that a breakglass account is created for AWS and follow best practices here"),
                False,
                'Task Finding - No Exceptions'
            ]
        ]
    )
    def test_finding(self, finding: Finding, ex: bool, description: str):
        if ex:
            self.assertIsInstance(finding, Finding, description)
        else:
            self.assertNotIsInstance(finding, Finding, description)

    @parameterized.expand(
        [
            [Violation(
                config_id='a.b.c',
                config_gap='Gap',
                config_fix='fix',
                config_value='9',
                preferred_value='10',
                additional_guidance='additional guidance',
                documentation='https://www.oak9.io',
                adjusted_severity=Severity.Moderate,
                severity=Severity.High
            ),
                'Design Gap Finding w/ Related Configs - No Exceptions'
            ]

        ]
    )
    def test_finding(self, finding: Finding, description: str):
        self.assertIsInstance(finding, Finding, description)


class ProxyTests(unittest.TestCase):

    # region ListerRule objects

    class LoadBalancer_ListenerRule_HostHeaderConfig:
        def __init__(self, values: List[str]):
            self.values = values

    class LoadBalancer_ListenerRule_QueryStringKeyValue:
        def __init__(self, key, value):
            self.key = key
            self.value = value

    class LoadBalancer_ListenerRule_QueryStringConfig:
        def __init__(self, values: List['ProxyTests.LoadBalancer_ListenerRule_QueryStringKeyValue']):
            self.values = values

    class LoadBalancer_ListenerRule_RuleCondition:
        def __init__(self, values: List[str],
                     host_header_config: 'ProxyTests.LoadBalancer_ListenerRule_HostHeaderConfig'):
            self.values = values
            self.host_header_config = host_header_config

    class LoadBalancerListenerRule:
        def __init__(self, conditions: List['ProxyTests.LoadBalancer_ListenerRule_RuleCondition']):
            self.conditions = conditions

    # endregion

    class LoadBalancerListener:
        def __init__(self):
            self.port = 80
            self.target_group_id = 'tg-123123'
            self.labels = ['lbl1', 'lbl2']

    class LoadBalancer:
        def __init__(self, name: str, tags: dict,
                     listeners: List['ProxyTests.LoadBalancerListener'],
                     listener_rules: List['ProxyTests.LoadBalancerListenerRule']):
            self.name = name
            self.tags = tags
            self.listeners = listeners
            self.listener_rules = listener_rules

    def setUp(self) -> None:
        listeners = [
            ProxyTests.LoadBalancerListener(),
            ProxyTests.LoadBalancerListener()
        ]
        listener_rules = [
            ProxyTests.LoadBalancerListenerRule([
                ProxyTests.LoadBalancer_ListenerRule_RuleCondition(
                    ['myval1', 'myval2'],
                    ProxyTests.LoadBalancer_ListenerRule_HostHeaderConfig(['X-CacheControl', 'X-CORS'])
                )
            ])
        ]
        actual_load_balancer = ProxyTests.LoadBalancer('my_lb', {'owner': 'joe'}, listeners, listener_rules)
        self.validation_resource = PathTrackerProxy.create(actual_load_balancer)

    def test_prop_string(self):
        prop = self.validation_resource.name
        self.assertEqual(prop, 'my_lb')
        self.assertTrue(prop == 'my_lb')
        self.assertTrue(prop != 'my_l')
        self.assertTrue(prop != 'MY_LB')

        prop_path = prop._id
        print(prop_path)
        self.assertEqual(prop_path, 'name')

    def test_prop_int(self):
        prop = self.validation_resource.listeners[0].port
        self.assertGreater(prop, 50)
        self.assertTrue(prop == 80)
        self.assertEqual(prop._id, 'listeners[0].port')

    def test_prop_list_of_strings(self):
        validation_resource = PathTrackerProxy.create(ProxyTests.LoadBalancerListener())
        prop = validation_resource.labels
        self.assertEqual(prop, ['lbl1', 'lbl2'])
        self.assertTrue(prop == ['lbl1', 'lbl2'])
        self.assertTrue('lbl1' in prop)
        self.assertFalse('LBL1' in prop)

        prop_path = prop._id
        print(prop_path)
        self.assertEqual(prop_path, 'labels')

        prop = validation_resource.labels[0]
        self.assertEqual(prop, 'lbl1')
        self.assertTrue(prop == 'lbl1')
        self.assertTrue('lbl1' in prop)
        self.assertFalse('LBL1' in prop)

        prop_path = prop._id
        print(prop_path)
        self.assertEqual(prop_path, 'labels[0]')

    def test_prop_accessing_the_property_multiple_times_doesnt_change_its_path(self):
        self.assertEqual(self.validation_resource.name, 'my_lb')
        self.assertTrue(self.validation_resource.name == 'my_lb')
        print(self.validation_resource.name._id)
        self.assertEqual(self.validation_resource.name._id, 'name')

    # region list of objects properties

    def test_prop_list_of_objects(self):
        prop = self.validation_resource.listeners
        self.assertEqual(len(prop), 2)

        prop_path = prop._id
        print(prop_path)
        self.assertEqual(prop_path, 'listeners')

    def test_prop_list_of_objects_index_access(self):
        prop = self.validation_resource.listeners[1].target_group_id
        self.assertEqual(prop, 'tg-123123')
        self.assertTrue(prop == 'tg-123123')

        prop_path = prop._id
        print(prop_path)
        self.assertEqual(prop_path, 'listeners[1].target_group_id')

    def test_prop_list_of_objects_foreach_access(self):
        listeners = self.validation_resource.listeners
        idx = 0
        for listener in listeners:
            prop = listener.target_group_id
            self.assertTrue(prop == 'tg-123123')
            self.assertEqual(prop, 'tg-123123')

            prop_path = prop._id
            print(prop_path)
            self.assertEqual(prop_path, f'listeners[{idx}].target_group_id')
            idx += 1

    def test_prop_list_of_objects_through_list_comprehension(self):
        listeners = self.validation_resource.listeners
        idx = 0
        for listener in [x for x in listeners]:
            prop = listener.target_group_id
            self.assertTrue(prop == 'tg-123123')
            self.assertEqual(prop, 'tg-123123')

            prop_path = prop._id
            print(prop_path)
            self.assertEqual(prop_path, f'listeners[{idx}].target_group_id')
            idx += 1

    def test_prop_deeply_nested_string(self):
        prop = self.validation_resource.listener_rules[0].conditions[0].host_header_config.values[0]

        self.assertTrue(prop == 'X-CacheControl')
        prop_path = prop._id
        print(prop_path)
        self.assertEqual(prop_path, f'listener_rules[0].conditions[0].host_header_config.values[0]')

        for rule in self.validation_resource.listener_rules:
            for condition in rule.conditions:
                for value in condition.host_header_config.values:
                    self.assertTrue(value == 'X-CacheControl')
                    self.assertEqual(prop_path, f'listener_rules[0].conditions[0].host_header_config.values[0]')
                    return

    # endregion

    # region properties of type dictionary

    def test_prop_dict(self):
        prop = self.validation_resource.tags
        self.assertEqual(prop, {'owner': 'joe'})

        prop_path = prop._id
        print(prop_path)
        self.assertEqual(prop_path, 'tags')

    def test_prop_dict_key_access(self):
        tags = self.validation_resource.tags
        prop = tags['owner']
        self.assertEqual(prop, 'joe')

        prop_path = prop._id
        print(prop_path)
        self.assertEqual(prop_path, 'tags[owner]')

    def test_prop_dict_get_method_access(self):
        tags = self.validation_resource.tags
        prop = tags.get('owner', None)
        self.assertEqual(prop, 'joe')

        prop_path = prop._id
        print(prop_path)
        self.assertEqual(prop_path, 'tags[owner]')

    def test_prop_dict_keys_method_access(self):
        tags = self.validation_resource.tags
        prop: List[str] = tags.keys()

        try:
            prop._id
            self.fail('dict.keys() should not return a PathTrackerProxy')
        except AttributeError:
            pass

        self.assertEqual(prop[0]._id, 'tags[owner]')

    def test_prop_dict_values_method_access(self):
        tags = self.validation_resource.tags
        prop: List[str] = tags.values()

        try:
            prop._id
            self.fail('dict.values() should not return a PathTrackerProxy')
        except AttributeError:
            pass

        self.assertEqual(prop[0]._id, 'tags[owner]')

    def test_prop_dict_items_method_access(self):
        tags = self.validation_resource.tags
        for key, value in tags.items():
            self.assertEqual(key, 'owner')
            self.assertEqual(key._id, 'tags[owner]')

            self.assertEqual(value, 'joe')
            self.assertEqual(value._id, 'tags[owner]')

    def test_proto(self):
        apigateway = ApiGatewayV2(api=Api(tags={'test':'eng'}))
        fixture = PathTrackerProxy.create(apigateway)
        got = fixture.api.tags._id
        want = 'api_gateway_v2.api.tags'
        self.assertEqual(want, got)
        for key,value in fixture.api.tags.items():
            self.assertEqual(f'api_gateway_v2.api.tags[{key}]', fixture.api.tags[key]._id)
            self.assertEqual('test',key)
            self.assertEqual('eng',fixture.api.tags[key])

    def test_proto_repeated(self):
        apigateway = ApiGatewayV2(api=Api(tags={'test':'eng'}), 
                                  stage=[Stage(stage_name='dev'),
                                  Stage(stage_name='prod',access_log_settings=
                                        StageAccessLogSettings(destination_arn="foo"))])
        fixture = PathTrackerProxy.create(apigateway)
        idx = 0
        values = ['', 'foo']
        for stage in fixture.stage:
            got = stage.access_log_settings.destination_arn._id
            want = f'api_gateway_v2.stage[{idx}].access_log_settings.destination_arn'
            self.assertEqual(want, got)
            self.assertEqual(values[idx], stage.access_log_settings.destination_arn)
            idx += 1

    def test_proto_lists(self):
        apigateway = ApiGatewayV2(api=Api(tags={'test':'eng'}, cors_configuration=ApiCors(allow_methods=['get','put'])))
        fixture = PathTrackerProxy.create(apigateway)
        want = ['get','put']
        self.assertEqual(want, fixture.api.cors_configuration.allow_methods)
        self.assertEqual('api_gateway_v2.api.cors_configuration.allow_methods', fixture.api.cors_configuration.allow_methods._id)

    def test_proto_bool(self):
        apigateway = ApiGatewayV2(route=[Route(api_key_required=True),Route(api_key_required=False)])
        fixture = PathTrackerProxy.create(apigateway)
        idx = 0
        values = [True, False]
        for route in fixture.route:
            self.assertEqual(values[idx],route.api_key_required)
            self.assertEqual(f'api_gateway_v2.route[{idx}].api_key_required',route.api_key_required._id)
            idx += 1

    def test_proto_ints(self):
        apigateway = ApiGatewayV2(api=Api(tags={'test':'eng'}, cors_configuration=ApiCors(allow_methods=['get','put'], max_age=10000)))
        fixture = PathTrackerProxy.create(apigateway)
        self.assertEqual(10000, fixture.api.cors_configuration.max_age)
        self.assertEqual('api_gateway_v2.api.cors_configuration.max_age', fixture.api.cors_configuration.max_age._id)

    def test_nested_dicts(self):
        class NestedDict:
            def __init__(self):
                self.tags = {'env': {'dev': 'us-east-1'}}

        nested_dict = NestedDict()
        nested_dict = PathTrackerProxy.create(nested_dict)
        self.assertEqual('tags[env][dev]',nested_dict.tags['env']['dev']._id)
        self.assertEqual('us-east-1',nested_dict.tags['env']['dev'])

    # endregion


if __name__ == '__main__':
    unittest.main()
