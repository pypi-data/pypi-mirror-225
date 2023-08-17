'''
# EZ Constructs

A collection of heaviliy opinionated AWS CDK highlevel constructs.
[construct.dev](https://constructs.dev/packages/ez-constructs/) || [npmjs](https://www.npmjs.com/package/ez-constructs)

## Installation

> The library requires AWS CDK version >= 2.7.0.

` npm install ez-constructs` or ` yarn add ez-constructs`

## Constructs

1. [SecureBucket](src/secure-bucket) - Creates an S3 bucket that is secure, encrypted at rest along with object retention and intelligent transition rules
2. [SimpleCodeBuildProject](src/codebuild-ci) - Creates Codebuild projects the easy way.

## Libraries

1. Utils - A collection of utility functions
2. CustomSynthesizer - A custom CDK synthesizer that will alter the default service roles that CDK uses.

## Aspects

1. [PermissionsBoundaryAspect](src/aspects) - A custom aspect that can be used to apply a permission boundary to all roles created in the contex.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_codebuild as _aws_cdk_aws_codebuild_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_events as _aws_cdk_aws_events_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import constructs as _constructs_77d1e7e8


class CustomSynthesizer(
    _aws_cdk_ceddda9d.DefaultStackSynthesizer,
    metaclass=jsii.JSIIMeta,
    jsii_type="ez-constructs.CustomSynthesizer",
):
    '''As a best practice organizations enforce policies which require all custom IAM Roles created to be defined under a specific path and permission boundary.

    In order to adhere with such compliance requirements, the CDK bootstrapping is often customized
    (refer: https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping.html#bootstrapping-customizing).
    So, we need to ensure that parallel customization is applied during synthesis phase.
    This Custom Synthesizer is used to modify the default path of the following IAM Roles internally used by CDK:

    - deploy role
    - file-publishing-role
    - image-publishing-role
    - cfn-exec-role
    - lookup-role

    :see:

    PermissionsBoundaryAspect *
    Example Usage::

    new DbStack(app, config.id('apiDbStack'), {
    env: {account: '123456789012', region: 'us-east-1'},
    synthesizer: new CustomSynthesizer('/banking/dev/'),
    });
    '''

    def __init__(self, role_path: builtins.str) -> None:
        '''
        :param role_path: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f080045a2d1faf66d212813fbca2f476c782734821039529b5317ec84381ea0)
            check_type(argname="argument role_path", value=role_path, expected_type=type_hints["role_path"])
        jsii.create(self.__class__, self, [role_path])


class EzConstruct(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="ez-constructs.EzConstruct",
):
    '''A marker base class for EzConstructs.'''

    def __init__(self, scope: _constructs_77d1e7e8.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fdbf166d776c14fb424ae19c70a3dd70710fd6ab1b72891c40c48c6bf133669)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])


@jsii.enum(jsii_type="ez-constructs.GitEvent")
class GitEvent(enum.Enum):
    '''The Github events which should trigger this build.'''

    PULL_REQUEST = "PULL_REQUEST"
    PUSH = "PUSH"
    ALL = "ALL"


@jsii.implements(_aws_cdk_ceddda9d.IAspect)
class PermissionsBoundaryAspect(
    metaclass=jsii.JSIIMeta,
    jsii_type="ez-constructs.PermissionsBoundaryAspect",
):
    '''As a best practice organizations enforce policies which require all custom IAM Roles created to be defined under a specific path and permission boundary.

    Well, this allows better governance and also prevents unintended privilege escalation.
    AWS CDK high level constructs and patterns encapsulates the role creation from end users.
    So it is a laborious and at times impossible to get a handle of newly created roles within a stack.
    This aspect will scan all roles within the given scope and will attach the right permission boundary and path to them.
    Example::

          const app = new App();
          const mystack = new MyStack(app, 'MyConstruct'); // assuming this will create a role by name `myCodeBuildRole` with admin access.
          Aspects.of(app).add(new PermissionsBoundaryAspect('/my/devroles/', 'boundary/dev-max'));
    '''

    def __init__(
        self,
        role_path: builtins.str,
        role_permission_boundary: builtins.str,
    ) -> None:
        '''Constructs a new PermissionsBoundaryAspect.

        :param role_path: - the role path to attach to newly created roles.
        :param role_permission_boundary: - the permission boundary to attach to newly created roles.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e21146239f529d4c7c7573ff7851541b6758a3373877082ded397d2b42f7191b)
            check_type(argname="argument role_path", value=role_path, expected_type=type_hints["role_path"])
            check_type(argname="argument role_permission_boundary", value=role_permission_boundary, expected_type=type_hints["role_permission_boundary"])
        jsii.create(self.__class__, self, [role_path, role_permission_boundary])

    @jsii.member(jsii_name="modifyRolePath")
    def modify_role_path(
        self,
        role_resource: _aws_cdk_aws_iam_ceddda9d.CfnRole,
        stack: _aws_cdk_ceddda9d.Stack,
    ) -> None:
        '''
        :param role_resource: -
        :param stack: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7536cb2f448fe953474186dc0747e81f4d8f437faec613ad0a8043185cb2e13a)
            check_type(argname="argument role_resource", value=role_resource, expected_type=type_hints["role_resource"])
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        return typing.cast(None, jsii.invoke(self, "modifyRolePath", [role_resource, stack]))

    @jsii.member(jsii_name="visit")
    def visit(self, node: _constructs_77d1e7e8.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e22d8b07bcff8691c4b3e0419e521f885cbcdc51a7ee4787a7d6d0c199db0c73)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))

    @builtins.property
    @jsii.member(jsii_name="rolePath")
    def role_path(self) -> builtins.str:
        '''The role path to attach to newly created roles.'''
        return typing.cast(builtins.str, jsii.get(self, "rolePath"))

    @role_path.setter
    def role_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8cd0f21c19e2033b3e7c69c2b0a81c07accb873a289c961a3d7df6dd2e442bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rolePath", value)

    @builtins.property
    @jsii.member(jsii_name="rolePermissionBoundary")
    def role_permission_boundary(self) -> builtins.str:
        '''The permission boundary to attach to newly created roles.'''
        return typing.cast(builtins.str, jsii.get(self, "rolePermissionBoundary"))

    @role_permission_boundary.setter
    def role_permission_boundary(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__546fd68c81f3db699e725f4e6c53647bf8bf3f2b58c323bb577c2708a254b991)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rolePermissionBoundary", value)


class SecureBucket(
    EzConstruct,
    metaclass=jsii.JSIIMeta,
    jsii_type="ez-constructs.SecureBucket",
):
    '''Will create a secure bucket with the following features: - Bucket name will be modified to include account and region.

    - Access limited to the owner
    - Object Versioning
    - Encryption at rest
    - Object expiration max limit to 10 years
    - Object will transition to IA after 60 days and later to deep archive after 365 days

    Example::

          let aBucket = new SecureBucket(mystack, 'secureBucket', {
            bucketName: 'mybucket',
            objectsExpireInDays: 500,
            enforceSSL: false,
           });
    '''

    def __init__(self, scope: _constructs_77d1e7e8.Construct, id: builtins.str) -> None:
        '''Creates the SecureBucket.

        :param scope: - the stack in which the construct is defined.
        :param id: - a unique identifier for the construct.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__908e4c242f627a2e004696fc9dbe99afa6a4112ac0e26b914170bfea97fc7fc7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])

    @jsii.member(jsii_name="assemble")
    def assemble(self) -> "SecureBucket":
        '''Creates the underlying S3 bucket.'''
        return typing.cast("SecureBucket", jsii.invoke(self, "assemble", []))

    @jsii.member(jsii_name="bucketName")
    def bucket_name(self, name: builtins.str) -> "SecureBucket":
        '''The name of the bucket.

        Internally the bucket name will be modified to include the account and region.

        :param name: - the name of the bucket to use.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05ad85e4cdbe8d1a4cbe881e16b9abc01d7592c4fbf6a27a9cd06ebfa2992c0d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast("SecureBucket", jsii.invoke(self, "bucketName", [name]))

    @jsii.member(jsii_name="moveToGlacierDeepArchive")
    def move_to_glacier_deep_archive(
        self,
        move: typing.Optional[builtins.bool] = None,
    ) -> "SecureBucket":
        '''Use only for buckets that have archiving data.

        CAUTION, once the object is archived, a temporary bucket to store the data.

        :param move: -

        :default: false

        :return: SecureBucket
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__385f51ace5c56604c3705866b979d82d67f1112e15faa48b4d7490adf0fe2182)
            check_type(argname="argument move", value=move, expected_type=type_hints["move"])
        return typing.cast("SecureBucket", jsii.invoke(self, "moveToGlacierDeepArchive", [move]))

    @jsii.member(jsii_name="objectsExpireInDays")
    def objects_expire_in_days(self, expiry_in_days: jsii.Number) -> "SecureBucket":
        '''The number of days that object will be kept.

        :param expiry_in_days: -

        :default: 3650 - 10 years

        :return: SecureBucket
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cd6f17f0446b65acf762c42683c8d61188c3ab03c4255e81be9306df2208e84)
            check_type(argname="argument expiry_in_days", value=expiry_in_days, expected_type=type_hints["expiry_in_days"])
        return typing.cast("SecureBucket", jsii.invoke(self, "objectsExpireInDays", [expiry_in_days]))

    @jsii.member(jsii_name="overrideBucketProperties")
    def override_bucket_properties(
        self,
        *,
        access_control: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketAccessControl] = None,
        auto_delete_objects: typing.Optional[builtins.bool] = None,
        block_public_access: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BlockPublicAccess] = None,
        bucket_key_enabled: typing.Optional[builtins.bool] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        cors: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.CorsRule, typing.Dict[builtins.str, typing.Any]]]] = None,
        encryption: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketEncryption] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        enforce_ssl: typing.Optional[builtins.bool] = None,
        event_bridge_enabled: typing.Optional[builtins.bool] = None,
        intelligent_tiering_configurations: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.IntelligentTieringConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
        inventories: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.Inventory, typing.Dict[builtins.str, typing.Any]]]] = None,
        lifecycle_rules: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.LifecycleRule, typing.Dict[builtins.str, typing.Any]]]] = None,
        metrics: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketMetrics, typing.Dict[builtins.str, typing.Any]]]] = None,
        notifications_handler_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        object_lock_default_retention: typing.Optional[_aws_cdk_aws_s3_ceddda9d.ObjectLockRetention] = None,
        object_lock_enabled: typing.Optional[builtins.bool] = None,
        object_ownership: typing.Optional[_aws_cdk_aws_s3_ceddda9d.ObjectOwnership] = None,
        public_read_access: typing.Optional[builtins.bool] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        server_access_logs_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
        server_access_logs_prefix: typing.Optional[builtins.str] = None,
        transfer_acceleration: typing.Optional[builtins.bool] = None,
        versioned: typing.Optional[builtins.bool] = None,
        website_error_document: typing.Optional[builtins.str] = None,
        website_index_document: typing.Optional[builtins.str] = None,
        website_redirect: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.RedirectTarget, typing.Dict[builtins.str, typing.Any]]] = None,
        website_routing_rules: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.RoutingRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> "SecureBucket":
        '''This function allows users to override the defaults calculated by this construct and is only recommended for advanced usecases.

        The values supplied via props superseeds the defaults that are calculated.

        :param access_control: Specifies a canned ACL that grants predefined permissions to the bucket. Default: BucketAccessControl.PRIVATE
        :param auto_delete_objects: Whether all objects should be automatically deleted when the bucket is removed from the stack or when the stack is deleted. Requires the ``removalPolicy`` to be set to ``RemovalPolicy.DESTROY``. **Warning** if you have deployed a bucket with ``autoDeleteObjects: true``, switching this to ``false`` in a CDK version *before* ``1.126.0`` will lead to all objects in the bucket being deleted. Be sure to update your bucket resources by deploying with CDK version ``1.126.0`` or later **before** switching this value to ``false``. Default: false
        :param block_public_access: The block public access configuration of this bucket. Default: - CloudFormation defaults will apply. New buckets and objects don't allow public access, but users can modify bucket policies or object permissions to allow public access
        :param bucket_key_enabled: Whether Amazon S3 should use its own intermediary key to generate data keys. Only relevant when using KMS for encryption. - If not enabled, every object GET and PUT will cause an API call to KMS (with the attendant cost implications of that). - If enabled, S3 will use its own time-limited key instead. Only relevant, when Encryption is set to ``BucketEncryption.KMS`` or ``BucketEncryption.KMS_MANAGED``. Default: - false
        :param bucket_name: Physical name of this bucket. Default: - Assigned by CloudFormation (recommended).
        :param cors: The CORS configuration of this bucket. Default: - No CORS configuration.
        :param encryption: The kind of server-side encryption to apply to this bucket. If you choose KMS, you can specify a KMS key via ``encryptionKey``. If encryption key is not specified, a key will automatically be created. Default: - ``KMS`` if ``encryptionKey`` is specified, or ``UNENCRYPTED`` otherwise. But if ``UNENCRYPTED`` is specified, the bucket will be encrypted as ``S3_MANAGED`` automatically.
        :param encryption_key: External KMS key to use for bucket encryption. The ``encryption`` property must be either not specified or set to ``KMS`` or ``DSSE``. An error will be emitted if ``encryption`` is set to ``UNENCRYPTED`` or ``S3_MANAGED``. Default: - If ``encryption`` is set to ``KMS`` and this property is undefined, a new KMS key will be created and associated with this bucket.
        :param enforce_ssl: Enforces SSL for requests. S3.5 of the AWS Foundational Security Best Practices Regarding S3. Default: false
        :param event_bridge_enabled: Whether this bucket should send notifications to Amazon EventBridge or not. Default: false
        :param intelligent_tiering_configurations: Inteligent Tiering Configurations. Default: No Intelligent Tiiering Configurations.
        :param inventories: The inventory configuration of the bucket. Default: - No inventory configuration
        :param lifecycle_rules: Rules that define how Amazon S3 manages objects during their lifetime. Default: - No lifecycle rules.
        :param metrics: The metrics configuration of this bucket. Default: - No metrics configuration.
        :param notifications_handler_role: The role to be used by the notifications handler. Default: - a new role will be created.
        :param object_lock_default_retention: The default retention mode and rules for S3 Object Lock. Default retention can be configured after a bucket is created if the bucket already has object lock enabled. Enabling object lock for existing buckets is not supported. Default: no default retention period
        :param object_lock_enabled: Enable object lock on the bucket. Enabling object lock for existing buckets is not supported. Object lock must be enabled when the bucket is created. Default: false, unless objectLockDefaultRetention is set (then, true)
        :param object_ownership: The objectOwnership of the bucket. Default: - No ObjectOwnership configuration, uploading account will own the object.
        :param public_read_access: Grants public read access to all objects in the bucket. Similar to calling ``bucket.grantPublicAccess()`` Default: false
        :param removal_policy: Policy to apply when the bucket is removed from this stack. Default: - The bucket will be orphaned.
        :param server_access_logs_bucket: Destination bucket for the server access logs. Default: - If "serverAccessLogsPrefix" undefined - access logs disabled, otherwise - log to current bucket.
        :param server_access_logs_prefix: Optional log file prefix to use for the bucket's access logs. If defined without "serverAccessLogsBucket", enables access logs to current bucket with this prefix. Default: - No log file prefix
        :param transfer_acceleration: Whether this bucket should have transfer acceleration turned on or not. Default: false
        :param versioned: Whether this bucket should have versioning turned on or not. Default: false (unless object lock is enabled, then true)
        :param website_error_document: The name of the error document (e.g. "404.html") for the website. ``websiteIndexDocument`` must also be set if this is set. Default: - No error document.
        :param website_index_document: The name of the index document (e.g. "index.html") for the website. Enables static website hosting for this bucket. Default: - No index document.
        :param website_redirect: Specifies the redirect behavior of all requests to a website endpoint of a bucket. If you specify this property, you can't specify "websiteIndexDocument", "websiteErrorDocument" nor , "websiteRoutingRules". Default: - No redirection.
        :param website_routing_rules: Rules that define when a redirect is applied and the redirect behavior. Default: - No redirection rules.

        :return: SecureBucket
        '''
        props = _aws_cdk_aws_s3_ceddda9d.BucketProps(
            access_control=access_control,
            auto_delete_objects=auto_delete_objects,
            block_public_access=block_public_access,
            bucket_key_enabled=bucket_key_enabled,
            bucket_name=bucket_name,
            cors=cors,
            encryption=encryption,
            encryption_key=encryption_key,
            enforce_ssl=enforce_ssl,
            event_bridge_enabled=event_bridge_enabled,
            intelligent_tiering_configurations=intelligent_tiering_configurations,
            inventories=inventories,
            lifecycle_rules=lifecycle_rules,
            metrics=metrics,
            notifications_handler_role=notifications_handler_role,
            object_lock_default_retention=object_lock_default_retention,
            object_lock_enabled=object_lock_enabled,
            object_ownership=object_ownership,
            public_read_access=public_read_access,
            removal_policy=removal_policy,
            server_access_logs_bucket=server_access_logs_bucket,
            server_access_logs_prefix=server_access_logs_prefix,
            transfer_acceleration=transfer_acceleration,
            versioned=versioned,
            website_error_document=website_error_document,
            website_index_document=website_index_document,
            website_redirect=website_redirect,
            website_routing_rules=website_routing_rules,
        )

        return typing.cast("SecureBucket", jsii.invoke(self, "overrideBucketProperties", [props]))

    @jsii.member(jsii_name="restrictAccessToIpOrCidrs")
    def restrict_access_to_ip_or_cidrs(
        self,
        ips_or_cidrs: typing.Sequence[builtins.str],
    ) -> "SecureBucket":
        '''Adds access restrictions so that the access is allowed from the following IP ranges.

        :param ips_or_cidrs: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a445329aae83234eb25a7889436044ae72824479be7f6dd3a0dd43bb43e13f18)
            check_type(argname="argument ips_or_cidrs", value=ips_or_cidrs, expected_type=type_hints["ips_or_cidrs"])
        return typing.cast("SecureBucket", jsii.invoke(self, "restrictAccessToIpOrCidrs", [ips_or_cidrs]))

    @jsii.member(jsii_name="restrictAccessToVpcs")
    def restrict_access_to_vpcs(
        self,
        vpc_ids: typing.Sequence[builtins.str],
    ) -> "SecureBucket":
        '''Adds access restrictions so that the access is allowed from the following VPCs.

        :param vpc_ids: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9df2fc6a514b96d44abe5a4affe599356f0f6ed5ba8b2a76fda9f0f63e17182)
            check_type(argname="argument vpc_ids", value=vpc_ids, expected_type=type_hints["vpc_ids"])
        return typing.cast("SecureBucket", jsii.invoke(self, "restrictAccessToVpcs", [vpc_ids]))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.Bucket]:
        '''The underlying S3 bucket created by this construct.'''
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.Bucket], jsii.get(self, "bucket"))


class SimpleCodebuildProject(
    EzConstruct,
    metaclass=jsii.JSIIMeta,
    jsii_type="ez-constructs.SimpleCodebuildProject",
):
    '''Most of the cases,a developer will use CodeBuild setup to perform simple CI tasks such as: - Build and test your code on a PR - Run a specific script based on a cron schedule.

    Also, they might want:

    - artifacts like testcase reports to be available via Reports UI and/or S3.
    - logs to be available via CloudWatch Logs.

    However, there can be additional organizational retention policies, for example retaining logs for a particular period of time.
    With this construct, you can easily create a basic CodeBuild project with many opinated defaults that are compliant with FISMA and NIST.

    Example, creates a project named ``my-project``, with artifacts going to my-project-artifacts--
    and logs going to ``/aws/codebuild/my-project`` log group with a retention period of 90 days and 14 months respectively::

          new SimpleCodebuildProject(stack, 'MyProject')
            .projectName('myproject')
            .gitRepoUrl('https://github.com/bijujoseph/cloudbiolinux.git')
            .gitBaseBranch('main')
            .triggerEvent(GitEvent.PULL_REQUEST)
            .buildSpecPath('buildspecs/my-pr-checker.yml')
            .assemble();
    '''

    def __init__(self, scope: _constructs_77d1e7e8.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a66fcdf6f2af25f3154e1a4b1df934ba9eff1e3f587a04803cc119aab6a986d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])

    @jsii.member(jsii_name="addEnv")
    def add_env(
        self,
        name: builtins.str,
        *,
        value: typing.Any,
        type: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.BuildEnvironmentVariableType] = None,
    ) -> "SimpleCodebuildProject":
        '''A convenient way to set the project environment variables.

        The values set here will be presnted on the UI when build with overriding is used.

        :param name: - The environment variable name.
        :param value: The value of the environment variable. For plain-text variables (the default), this is the literal value of variable. For SSM parameter variables, pass the name of the parameter here (``parameterName`` property of ``IParameter``). For SecretsManager variables secrets, pass either the secret name (``secretName`` property of ``ISecret``) or the secret ARN (``secretArn`` property of ``ISecret``) here, along with optional SecretsManager qualifiers separated by ':', like the JSON key, or the version or stage (see https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html#build-spec.env.secrets-manager for details).
        :param type: The type of environment variable. Default: PlainText
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3733264320f290806ce522f27e6c23161f8f2f6da49f36230c02fe8ea66873a4)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        env_var = _aws_cdk_aws_codebuild_ceddda9d.BuildEnvironmentVariable(
            value=value, type=type
        )

        return typing.cast("SimpleCodebuildProject", jsii.invoke(self, "addEnv", [name, env_var]))

    @jsii.member(jsii_name="artifactBucket")
    def artifact_bucket(
        self,
        artifact_bucket: typing.Union[builtins.str, _aws_cdk_aws_s3_ceddda9d.IBucket],
    ) -> "SimpleCodebuildProject":
        '''The name of the bucket to store the artifacts.

        By default the buckets will get stored in ``<project-name>-artifacts`` bucket.
        This function can be used to ovrride the default behavior.

        :param artifact_bucket: - a valid existing Bucket reference or bucket name to use.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdc95533cf1c5cf2eab607fe9ba11252f53631e12a644443f836c8f9cf47a021)
            check_type(argname="argument artifact_bucket", value=artifact_bucket, expected_type=type_hints["artifact_bucket"])
        return typing.cast("SimpleCodebuildProject", jsii.invoke(self, "artifactBucket", [artifact_bucket]))

    @jsii.member(jsii_name="assemble")
    def assemble(
        self,
        *,
        artifacts: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.IArtifacts] = None,
        secondary_artifacts: typing.Optional[typing.Sequence[_aws_cdk_aws_codebuild_ceddda9d.IArtifacts]] = None,
        secondary_sources: typing.Optional[typing.Sequence[_aws_cdk_aws_codebuild_ceddda9d.ISource]] = None,
        source: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.ISource] = None,
        allow_all_outbound: typing.Optional[builtins.bool] = None,
        badge: typing.Optional[builtins.bool] = None,
        build_spec: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.BuildSpec] = None,
        cache: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.Cache] = None,
        check_secrets_in_plain_text_env_variables: typing.Optional[builtins.bool] = None,
        concurrent_build_limit: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        environment: typing.Optional[typing.Union[_aws_cdk_aws_codebuild_ceddda9d.BuildEnvironment, typing.Dict[builtins.str, typing.Any]]] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_codebuild_ceddda9d.BuildEnvironmentVariable, typing.Dict[builtins.str, typing.Any]]]] = None,
        file_system_locations: typing.Optional[typing.Sequence[_aws_cdk_aws_codebuild_ceddda9d.IFileSystemLocation]] = None,
        grant_report_group_permissions: typing.Optional[builtins.bool] = None,
        logging: typing.Optional[typing.Union[_aws_cdk_aws_codebuild_ceddda9d.LoggingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        project_name: typing.Optional[builtins.str] = None,
        queued_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        ssm_session_permissions: typing.Optional[builtins.bool] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> "SimpleCodebuildProject":
        '''
        :param artifacts: Defines where build artifacts will be stored. Could be: PipelineBuildArtifacts, NoArtifacts and S3Artifacts. Default: NoArtifacts
        :param secondary_artifacts: The secondary artifacts for the Project. Can also be added after the Project has been created by using the ``Project#addSecondaryArtifact`` method. Default: - No secondary artifacts.
        :param secondary_sources: The secondary sources for the Project. Can be also added after the Project has been created by using the ``Project#addSecondarySource`` method. Default: - No secondary sources.
        :param source: The source of the build. *Note*: if ``NoSource`` is given as the source, then you need to provide an explicit ``buildSpec``. Default: - NoSource
        :param allow_all_outbound: Whether to allow the CodeBuild to send all network traffic. If set to false, you must individually add traffic rules to allow the CodeBuild project to connect to network targets. Only used if 'vpc' is supplied. Default: true
        :param badge: Indicates whether AWS CodeBuild generates a publicly accessible URL for your project's build badge. For more information, see Build Badges Sample in the AWS CodeBuild User Guide. Default: false
        :param build_spec: Filename or contents of buildspec in JSON format. Default: - Empty buildspec.
        :param cache: Caching strategy to use. Default: Cache.none
        :param check_secrets_in_plain_text_env_variables: Whether to check for the presence of any secrets in the environment variables of the default type, BuildEnvironmentVariableType.PLAINTEXT. Since using a secret for the value of that kind of variable would result in it being displayed in plain text in the AWS Console, the construct will throw an exception if it detects a secret was passed there. Pass this property as false if you want to skip this validation, and keep using a secret in a plain text environment variable. Default: true
        :param concurrent_build_limit: Maximum number of concurrent builds. Minimum value is 1 and maximum is account build limit. Default: - no explicit limit is set
        :param description: A description of the project. Use the description to identify the purpose of the project. Default: - No description.
        :param encryption_key: Encryption key to use to read and write artifacts. Default: - The AWS-managed CMK for Amazon Simple Storage Service (Amazon S3) is used.
        :param environment: Build environment to use for the build. Default: BuildEnvironment.LinuxBuildImage.STANDARD_1_0
        :param environment_variables: Additional environment variables to add to the build environment. Default: - No additional environment variables are specified.
        :param file_system_locations: An ProjectFileSystemLocation objects for a CodeBuild build project. A ProjectFileSystemLocation object specifies the identifier, location, mountOptions, mountPoint, and type of a file system created using Amazon Elastic File System. Default: - no file system locations
        :param grant_report_group_permissions: Add permissions to this project's role to create and use test report groups with name starting with the name of this project. That is the standard report group that gets created when a simple name (in contrast to an ARN) is used in the 'reports' section of the buildspec of this project. This is usually harmless, but you can turn these off if you don't plan on using test reports in this project. Default: true
        :param logging: Information about logs for the build project. A project can create logs in Amazon CloudWatch Logs, an S3 bucket, or both. Default: - no log configuration is set
        :param project_name: The physical, human-readable name of the CodeBuild Project. Default: - Name is automatically generated.
        :param queued_timeout: The number of minutes after which AWS CodeBuild stops the build if it's still in queue. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: - no queue timeout is set
        :param role: Service Role to assume while running the build. Default: - A role will be created.
        :param security_groups: What security group to associate with the codebuild project's network interfaces. If no security group is identified, one will be created automatically. Only used if 'vpc' is supplied. Default: - Security group will be automatically created.
        :param ssm_session_permissions: Add the permissions necessary for debugging builds with SSM Session Manager. If the following prerequisites have been met: - The necessary permissions have been added by setting this flag to true. - The build image has the SSM agent installed (true for default CodeBuild images). - The build is started with `debugSessionEnabled <https://docs.aws.amazon.com/codebuild/latest/APIReference/API_StartBuild.html#CodeBuild-StartBuild-request-debugSessionEnabled>`_ set to true. Then the build container can be paused and inspected using Session Manager by invoking the ``codebuild-breakpoint`` command somewhere during the build. ``codebuild-breakpoint`` commands will be ignored if the build is not started with ``debugSessionEnabled=true``. Default: false
        :param subnet_selection: Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param timeout: The number of minutes after which AWS CodeBuild stops the build if it's not complete. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: Duration.hours(1)
        :param vpc: VPC network to place codebuild network interfaces. Specify this if the codebuild project needs to access resources in a VPC. Default: - No VPC is specified.
        '''
        default_props = _aws_cdk_aws_codebuild_ceddda9d.ProjectProps(
            artifacts=artifacts,
            secondary_artifacts=secondary_artifacts,
            secondary_sources=secondary_sources,
            source=source,
            allow_all_outbound=allow_all_outbound,
            badge=badge,
            build_spec=build_spec,
            cache=cache,
            check_secrets_in_plain_text_env_variables=check_secrets_in_plain_text_env_variables,
            concurrent_build_limit=concurrent_build_limit,
            description=description,
            encryption_key=encryption_key,
            environment=environment,
            environment_variables=environment_variables,
            file_system_locations=file_system_locations,
            grant_report_group_permissions=grant_report_group_permissions,
            logging=logging,
            project_name=project_name,
            queued_timeout=queued_timeout,
            role=role,
            security_groups=security_groups,
            ssm_session_permissions=ssm_session_permissions,
            subnet_selection=subnet_selection,
            timeout=timeout,
            vpc=vpc,
        )

        return typing.cast("SimpleCodebuildProject", jsii.invoke(self, "assemble", [default_props]))

    @jsii.member(jsii_name="buildImage")
    def build_image(
        self,
        build_image: _aws_cdk_aws_codebuild_ceddda9d.IBuildImage,
    ) -> "SimpleCodebuildProject":
        '''The build image to use.

        :param build_image: -

        :see: https://docs.aws.amazon.com/cdk/api/v1/docs/@aws-cdk_aws-codebuild.IBuildImage.html
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cf56db7e7ceadd109b72955351f50aa4ade48fd0defb958d11bf0f86b40ea3f)
            check_type(argname="argument build_image", value=build_image, expected_type=type_hints["build_image"])
        return typing.cast("SimpleCodebuildProject", jsii.invoke(self, "buildImage", [build_image]))

    @jsii.member(jsii_name="buildSpecPath")
    def build_spec_path(
        self,
        build_spec_path: builtins.str,
    ) -> "SimpleCodebuildProject":
        '''The build spec file path.

        :param build_spec_path: - relative location of the build spec file.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1bb98c3cfc225986b950e6f83f0e796b4a823a143028aedc3b930054e71514d)
            check_type(argname="argument build_spec_path", value=build_spec_path, expected_type=type_hints["build_spec_path"])
        return typing.cast("SimpleCodebuildProject", jsii.invoke(self, "buildSpecPath", [build_spec_path]))

    @jsii.member(jsii_name="computeType")
    def compute_type(
        self,
        compute_type: _aws_cdk_aws_codebuild_ceddda9d.ComputeType,
    ) -> "SimpleCodebuildProject":
        '''The compute type to use.

        :param compute_type: -

        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-compute-types.html
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2cd9097c8359b9f10b12297798c0fb088fd2bbf92300417ac595d9d2f1033cb)
            check_type(argname="argument compute_type", value=compute_type, expected_type=type_hints["compute_type"])
        return typing.cast("SimpleCodebuildProject", jsii.invoke(self, "computeType", [compute_type]))

    @jsii.member(jsii_name="ecrBuildImage")
    def ecr_build_image(
        self,
        ecr_repo_name: builtins.str,
        image_tag: builtins.str,
    ) -> "SimpleCodebuildProject":
        '''The build image to use.

        :param ecr_repo_name: - the ecr repository name.
        :param image_tag: - the image tag.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa9f0b42fab79908b5cac6faf51d6b3eab50111ac8cf2227689fff40dc06b3bf)
            check_type(argname="argument ecr_repo_name", value=ecr_repo_name, expected_type=type_hints["ecr_repo_name"])
            check_type(argname="argument image_tag", value=image_tag, expected_type=type_hints["image_tag"])
        return typing.cast("SimpleCodebuildProject", jsii.invoke(self, "ecrBuildImage", [ecr_repo_name, image_tag]))

    @jsii.member(jsii_name="gitBaseBranch")
    def git_base_branch(self, branch: builtins.str) -> "SimpleCodebuildProject":
        '''The main branch of the github project.

        :param branch: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c95f063a065ad74e68c7ae6e353999d36d70da844c234c01d1eae907d50ac116)
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
        return typing.cast("SimpleCodebuildProject", jsii.invoke(self, "gitBaseBranch", [branch]))

    @jsii.member(jsii_name="gitRepoUrl")
    def git_repo_url(self, git_repo_url: builtins.str) -> "SimpleCodebuildProject":
        '''The github or enterprise github repository url.

        :param git_repo_url: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff9fa5a15e686d115ee6fc23bb85d6942edfd12793e7d8cdfb51b12c7bd91d58)
            check_type(argname="argument git_repo_url", value=git_repo_url, expected_type=type_hints["git_repo_url"])
        return typing.cast("SimpleCodebuildProject", jsii.invoke(self, "gitRepoUrl", [git_repo_url]))

    @jsii.member(jsii_name="inVpc")
    def in_vpc(self, vpc_id: builtins.str) -> "SimpleCodebuildProject":
        '''The vpc network interfaces to add to the codebuild.

        :param vpc_id: -

        :see: https://docs.aws.amazon.com/cdk/api/v1/docs/aws-codebuild-readme.html#definition-of-vpc-configuration-in-codebuild-project
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__457187e968eb632c4dc3501b812b4f38e0dbe9a0ba3ce22b6deca7c3e3f550ea)
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        return typing.cast("SimpleCodebuildProject", jsii.invoke(self, "inVpc", [vpc_id]))

    @jsii.member(jsii_name="overrideProjectProps")
    def override_project_props(
        self,
        *,
        artifacts: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.IArtifacts] = None,
        secondary_artifacts: typing.Optional[typing.Sequence[_aws_cdk_aws_codebuild_ceddda9d.IArtifacts]] = None,
        secondary_sources: typing.Optional[typing.Sequence[_aws_cdk_aws_codebuild_ceddda9d.ISource]] = None,
        source: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.ISource] = None,
        allow_all_outbound: typing.Optional[builtins.bool] = None,
        badge: typing.Optional[builtins.bool] = None,
        build_spec: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.BuildSpec] = None,
        cache: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.Cache] = None,
        check_secrets_in_plain_text_env_variables: typing.Optional[builtins.bool] = None,
        concurrent_build_limit: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        environment: typing.Optional[typing.Union[_aws_cdk_aws_codebuild_ceddda9d.BuildEnvironment, typing.Dict[builtins.str, typing.Any]]] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_codebuild_ceddda9d.BuildEnvironmentVariable, typing.Dict[builtins.str, typing.Any]]]] = None,
        file_system_locations: typing.Optional[typing.Sequence[_aws_cdk_aws_codebuild_ceddda9d.IFileSystemLocation]] = None,
        grant_report_group_permissions: typing.Optional[builtins.bool] = None,
        logging: typing.Optional[typing.Union[_aws_cdk_aws_codebuild_ceddda9d.LoggingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        project_name: typing.Optional[builtins.str] = None,
        queued_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        ssm_session_permissions: typing.Optional[builtins.bool] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> "SimpleCodebuildProject":
        '''
        :param artifacts: Defines where build artifacts will be stored. Could be: PipelineBuildArtifacts, NoArtifacts and S3Artifacts. Default: NoArtifacts
        :param secondary_artifacts: The secondary artifacts for the Project. Can also be added after the Project has been created by using the ``Project#addSecondaryArtifact`` method. Default: - No secondary artifacts.
        :param secondary_sources: The secondary sources for the Project. Can be also added after the Project has been created by using the ``Project#addSecondarySource`` method. Default: - No secondary sources.
        :param source: The source of the build. *Note*: if ``NoSource`` is given as the source, then you need to provide an explicit ``buildSpec``. Default: - NoSource
        :param allow_all_outbound: Whether to allow the CodeBuild to send all network traffic. If set to false, you must individually add traffic rules to allow the CodeBuild project to connect to network targets. Only used if 'vpc' is supplied. Default: true
        :param badge: Indicates whether AWS CodeBuild generates a publicly accessible URL for your project's build badge. For more information, see Build Badges Sample in the AWS CodeBuild User Guide. Default: false
        :param build_spec: Filename or contents of buildspec in JSON format. Default: - Empty buildspec.
        :param cache: Caching strategy to use. Default: Cache.none
        :param check_secrets_in_plain_text_env_variables: Whether to check for the presence of any secrets in the environment variables of the default type, BuildEnvironmentVariableType.PLAINTEXT. Since using a secret for the value of that kind of variable would result in it being displayed in plain text in the AWS Console, the construct will throw an exception if it detects a secret was passed there. Pass this property as false if you want to skip this validation, and keep using a secret in a plain text environment variable. Default: true
        :param concurrent_build_limit: Maximum number of concurrent builds. Minimum value is 1 and maximum is account build limit. Default: - no explicit limit is set
        :param description: A description of the project. Use the description to identify the purpose of the project. Default: - No description.
        :param encryption_key: Encryption key to use to read and write artifacts. Default: - The AWS-managed CMK for Amazon Simple Storage Service (Amazon S3) is used.
        :param environment: Build environment to use for the build. Default: BuildEnvironment.LinuxBuildImage.STANDARD_1_0
        :param environment_variables: Additional environment variables to add to the build environment. Default: - No additional environment variables are specified.
        :param file_system_locations: An ProjectFileSystemLocation objects for a CodeBuild build project. A ProjectFileSystemLocation object specifies the identifier, location, mountOptions, mountPoint, and type of a file system created using Amazon Elastic File System. Default: - no file system locations
        :param grant_report_group_permissions: Add permissions to this project's role to create and use test report groups with name starting with the name of this project. That is the standard report group that gets created when a simple name (in contrast to an ARN) is used in the 'reports' section of the buildspec of this project. This is usually harmless, but you can turn these off if you don't plan on using test reports in this project. Default: true
        :param logging: Information about logs for the build project. A project can create logs in Amazon CloudWatch Logs, an S3 bucket, or both. Default: - no log configuration is set
        :param project_name: The physical, human-readable name of the CodeBuild Project. Default: - Name is automatically generated.
        :param queued_timeout: The number of minutes after which AWS CodeBuild stops the build if it's still in queue. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: - no queue timeout is set
        :param role: Service Role to assume while running the build. Default: - A role will be created.
        :param security_groups: What security group to associate with the codebuild project's network interfaces. If no security group is identified, one will be created automatically. Only used if 'vpc' is supplied. Default: - Security group will be automatically created.
        :param ssm_session_permissions: Add the permissions necessary for debugging builds with SSM Session Manager. If the following prerequisites have been met: - The necessary permissions have been added by setting this flag to true. - The build image has the SSM agent installed (true for default CodeBuild images). - The build is started with `debugSessionEnabled <https://docs.aws.amazon.com/codebuild/latest/APIReference/API_StartBuild.html#CodeBuild-StartBuild-request-debugSessionEnabled>`_ set to true. Then the build container can be paused and inspected using Session Manager by invoking the ``codebuild-breakpoint`` command somewhere during the build. ``codebuild-breakpoint`` commands will be ignored if the build is not started with ``debugSessionEnabled=true``. Default: false
        :param subnet_selection: Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param timeout: The number of minutes after which AWS CodeBuild stops the build if it's not complete. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: Duration.hours(1)
        :param vpc: VPC network to place codebuild network interfaces. Specify this if the codebuild project needs to access resources in a VPC. Default: - No VPC is specified.
        '''
        props = _aws_cdk_aws_codebuild_ceddda9d.ProjectProps(
            artifacts=artifacts,
            secondary_artifacts=secondary_artifacts,
            secondary_sources=secondary_sources,
            source=source,
            allow_all_outbound=allow_all_outbound,
            badge=badge,
            build_spec=build_spec,
            cache=cache,
            check_secrets_in_plain_text_env_variables=check_secrets_in_plain_text_env_variables,
            concurrent_build_limit=concurrent_build_limit,
            description=description,
            encryption_key=encryption_key,
            environment=environment,
            environment_variables=environment_variables,
            file_system_locations=file_system_locations,
            grant_report_group_permissions=grant_report_group_permissions,
            logging=logging,
            project_name=project_name,
            queued_timeout=queued_timeout,
            role=role,
            security_groups=security_groups,
            ssm_session_permissions=ssm_session_permissions,
            subnet_selection=subnet_selection,
            timeout=timeout,
            vpc=vpc,
        )

        return typing.cast("SimpleCodebuildProject", jsii.invoke(self, "overrideProjectProps", [props]))

    @jsii.member(jsii_name="privileged")
    def privileged(self, p: builtins.bool) -> "SimpleCodebuildProject":
        '''Set privileged mode of execution.

        Usually needed if this project builds Docker images,
        and the build environment image you chose is not provided by CodeBuild with Docker support.
        By default, Docker containers do not allow access to any devices.
        Privileged mode grants a build project's Docker container access to all devices
        https://docs.aws.amazon.com/codebuild/latest/userguide/change-project-console.html#change-project-console-environment

        :param p: - true/false.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49a1de8fe00c26dbdd5f0353f96b074e2154998cb331e299fb76a9a1a2bc4919)
            check_type(argname="argument p", value=p, expected_type=type_hints["p"])
        return typing.cast("SimpleCodebuildProject", jsii.invoke(self, "privileged", [p]))

    @jsii.member(jsii_name="projectDescription")
    def project_description(
        self,
        project_description: builtins.str,
    ) -> "SimpleCodebuildProject":
        '''The description of the codebuild project.

        :param project_description: - a valid description string.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cec20d71b6e66d417a7cbbf29f4582feb6048ded9c9a511d16e02645e8bed25)
            check_type(argname="argument project_description", value=project_description, expected_type=type_hints["project_description"])
        return typing.cast("SimpleCodebuildProject", jsii.invoke(self, "projectDescription", [project_description]))

    @jsii.member(jsii_name="projectName")
    def project_name(self, project_name: builtins.str) -> "SimpleCodebuildProject":
        '''The name of the codebuild project.

        :param project_name: - a valid name string.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47c7b8991f69deb3dce291d9511e8c90ad87a5c51470a6a7dc10efb61019d78f)
            check_type(argname="argument project_name", value=project_name, expected_type=type_hints["project_name"])
        return typing.cast("SimpleCodebuildProject", jsii.invoke(self, "projectName", [project_name]))

    @jsii.member(jsii_name="triggerBuildOnGitEvent")
    def trigger_build_on_git_event(self, event: GitEvent) -> "SimpleCodebuildProject":
        '''The Github events that can trigger this build.

        :param event: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d751bc8805262cceaff1945b81da131bd1b279a3e8970c0bfffcaa08d1a9518)
            check_type(argname="argument event", value=event, expected_type=type_hints["event"])
        return typing.cast("SimpleCodebuildProject", jsii.invoke(self, "triggerBuildOnGitEvent", [event]))

    @jsii.member(jsii_name="triggerBuildOnSchedule")
    def trigger_build_on_schedule(
        self,
        schedule: _aws_cdk_aws_events_ceddda9d.Schedule,
    ) -> "SimpleCodebuildProject":
        '''The cron schedule on which this build gets triggerd.

        :param schedule: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70a2d54e99153d760066833565fc99621b594db93de0feeee3bd192a25a7cd90)
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        return typing.cast("SimpleCodebuildProject", jsii.invoke(self, "triggerBuildOnSchedule", [schedule]))

    @jsii.member(jsii_name="triggerOnPushToBranches")
    def trigger_on_push_to_branches(
        self,
        branches: typing.Sequence[builtins.str],
    ) -> "SimpleCodebuildProject":
        '''Triggers build on push to specified branches.

        :param branches: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__371ef1a2fffc32327bc9a3d0ae0bb69ceb73341de5c1a9bc545eb466594723b5)
            check_type(argname="argument branches", value=branches, expected_type=type_hints["branches"])
        return typing.cast("SimpleCodebuildProject", jsii.invoke(self, "triggerOnPushToBranches", [branches]))

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.Project]:
        '''The underlying codebuild project that is created by this construct.'''
        return typing.cast(typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.Project], jsii.get(self, "project"))


class Utils(metaclass=jsii.JSIIMeta, jsii_type="ez-constructs.Utils"):
    '''A utility class that have common functions.'''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="appendIfNecessary")
    @builtins.classmethod
    def append_if_necessary(
        cls,
        name: builtins.str,
        *suffixes: builtins.str,
    ) -> builtins.str:
        '''Will append the suffix to the given name if the name do not contain the suffix.

        :param name: - a string.
        :param suffixes: - the string to append.

        :return: the name with the suffix appended if necessary delimited by a hyphen
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab7d624c4b17ae5798d2698454d6664a420296e02d5be3d3594785bdcecf3128)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument suffixes", value=suffixes, expected_type=typing.Tuple[type_hints["suffixes"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(builtins.str, jsii.sinvoke(cls, "appendIfNecessary", [name, *suffixes]))

    @jsii.member(jsii_name="endsWith")
    @builtins.classmethod
    def ends_with(cls, str: builtins.str, s: builtins.str) -> builtins.bool:
        '''Will check if the given string ends with the given suffix.

        :param str: - a string.
        :param s: - suffix to check.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2992ae92902d8b81668ae7355ad4ea4ac8db2b07a12cd50a42be7f9e50929264)
            check_type(argname="argument str", value=str, expected_type=type_hints["str"])
            check_type(argname="argument s", value=s, expected_type=type_hints["s"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "endsWith", [str, s]))

    @jsii.member(jsii_name="isEmpty")
    @builtins.classmethod
    def is_empty(cls, value: typing.Any = None) -> builtins.bool:
        '''Will check if the given object is empty.

        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__350c5bb98e107eee6ee21ce2e7e012972cbae0b757a37bd6ee1f5e66025eec9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isEmpty", [value]))

    @jsii.member(jsii_name="kebabCase")
    @builtins.classmethod
    def kebab_case(cls, str: builtins.str) -> builtins.str:
        '''Will convert the given string to lower case and transform any spaces to hyphens.

        :param str: - a string.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0e4526132686dd17a76cbc5266bbd91f6ff16cdccfd3fd6245f1061a6ff514d)
            check_type(argname="argument str", value=str, expected_type=type_hints["str"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "kebabCase", [str]))

    @jsii.member(jsii_name="parseGithubUrl")
    @builtins.classmethod
    def parse_github_url(cls, url: builtins.str) -> typing.Any:
        '''Splits a given Github URL and extracts the owner and repo name.

        :param url: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a691b7ad10e5308aff51aa2082dc54b2a1b1cc77ade0cae68b1ecf78fba856a)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        return typing.cast(typing.Any, jsii.sinvoke(cls, "parseGithubUrl", [url]))

    @jsii.member(jsii_name="prettyPrintStack")
    @builtins.classmethod
    def pretty_print_stack(
        cls,
        stack: _aws_cdk_ceddda9d.Stack,
        persist: typing.Optional[builtins.bool] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''A utility function that will print the content of a CDK stack.

        :param stack: - a valid stack.
        :param persist: -
        :param path: -

        :warning: This function is only used for debugging purpose.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e64ebb7228e613203bd98f40a1ff8cfe6b40703167a883bb3f0a0c727a79d2e7)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
            check_type(argname="argument persist", value=persist, expected_type=type_hints["persist"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast(None, jsii.sinvoke(cls, "prettyPrintStack", [stack, persist, path]))

    @jsii.member(jsii_name="startsWith")
    @builtins.classmethod
    def starts_with(cls, str: builtins.str, s: builtins.str) -> builtins.bool:
        '''Will check if the given string starts with the given prefix.

        :param str: - a string.
        :param s: - the prefix to check.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4503a468a48cac5f6781501429a0ca70194cff93e94a9f9c1b72e64161ff096f)
            check_type(argname="argument str", value=str, expected_type=type_hints["str"])
            check_type(argname="argument s", value=s, expected_type=type_hints["s"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "startsWith", [str, s]))

    @jsii.member(jsii_name="suppressNagRule")
    @builtins.classmethod
    def suppress_nag_rule(
        cls,
        scope: _constructs_77d1e7e8.IConstruct,
        rule_id: builtins.str,
        reason: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Will disable the CDK NAG rule for the given construct and its children.

        :param scope: - the scope to disable the rule for.
        :param rule_id: - the rule id to disable.
        :param reason: - reason for disabling the rule.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2d5b06f249e7a0f41e6e205451860c1add18aeaa6bef4e833f655e2b1694860)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument rule_id", value=rule_id, expected_type=type_hints["rule_id"])
            check_type(argname="argument reason", value=reason, expected_type=type_hints["reason"])
        return typing.cast(None, jsii.sinvoke(cls, "suppressNagRule", [scope, rule_id, reason]))

    @jsii.member(jsii_name="wrap")
    @builtins.classmethod
    def wrap(cls, str: builtins.str, delimiter: builtins.str) -> builtins.str:
        '''Will wrap the given string using the given delimiter.

        :param str: - the string to wrap.
        :param delimiter: - the delimiter to use.

        :return: the wrapped string
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8335787277838180e459986b4f0f134fb3f147e37b0038a91887173bd63c7ecc)
            check_type(argname="argument str", value=str, expected_type=type_hints["str"])
            check_type(argname="argument delimiter", value=delimiter, expected_type=type_hints["delimiter"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "wrap", [str, delimiter]))


__all__ = [
    "CustomSynthesizer",
    "EzConstruct",
    "GitEvent",
    "PermissionsBoundaryAspect",
    "SecureBucket",
    "SimpleCodebuildProject",
    "Utils",
]

publication.publish()

def _typecheckingstub__4f080045a2d1faf66d212813fbca2f476c782734821039529b5317ec84381ea0(
    role_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fdbf166d776c14fb424ae19c70a3dd70710fd6ab1b72891c40c48c6bf133669(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e21146239f529d4c7c7573ff7851541b6758a3373877082ded397d2b42f7191b(
    role_path: builtins.str,
    role_permission_boundary: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7536cb2f448fe953474186dc0747e81f4d8f437faec613ad0a8043185cb2e13a(
    role_resource: _aws_cdk_aws_iam_ceddda9d.CfnRole,
    stack: _aws_cdk_ceddda9d.Stack,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e22d8b07bcff8691c4b3e0419e521f885cbcdc51a7ee4787a7d6d0c199db0c73(
    node: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8cd0f21c19e2033b3e7c69c2b0a81c07accb873a289c961a3d7df6dd2e442bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__546fd68c81f3db699e725f4e6c53647bf8bf3f2b58c323bb577c2708a254b991(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__908e4c242f627a2e004696fc9dbe99afa6a4112ac0e26b914170bfea97fc7fc7(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05ad85e4cdbe8d1a4cbe881e16b9abc01d7592c4fbf6a27a9cd06ebfa2992c0d(
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__385f51ace5c56604c3705866b979d82d67f1112e15faa48b4d7490adf0fe2182(
    move: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cd6f17f0446b65acf762c42683c8d61188c3ab03c4255e81be9306df2208e84(
    expiry_in_days: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a445329aae83234eb25a7889436044ae72824479be7f6dd3a0dd43bb43e13f18(
    ips_or_cidrs: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9df2fc6a514b96d44abe5a4affe599356f0f6ed5ba8b2a76fda9f0f63e17182(
    vpc_ids: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a66fcdf6f2af25f3154e1a4b1df934ba9eff1e3f587a04803cc119aab6a986d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3733264320f290806ce522f27e6c23161f8f2f6da49f36230c02fe8ea66873a4(
    name: builtins.str,
    *,
    value: typing.Any,
    type: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.BuildEnvironmentVariableType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdc95533cf1c5cf2eab607fe9ba11252f53631e12a644443f836c8f9cf47a021(
    artifact_bucket: typing.Union[builtins.str, _aws_cdk_aws_s3_ceddda9d.IBucket],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cf56db7e7ceadd109b72955351f50aa4ade48fd0defb958d11bf0f86b40ea3f(
    build_image: _aws_cdk_aws_codebuild_ceddda9d.IBuildImage,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1bb98c3cfc225986b950e6f83f0e796b4a823a143028aedc3b930054e71514d(
    build_spec_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2cd9097c8359b9f10b12297798c0fb088fd2bbf92300417ac595d9d2f1033cb(
    compute_type: _aws_cdk_aws_codebuild_ceddda9d.ComputeType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa9f0b42fab79908b5cac6faf51d6b3eab50111ac8cf2227689fff40dc06b3bf(
    ecr_repo_name: builtins.str,
    image_tag: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c95f063a065ad74e68c7ae6e353999d36d70da844c234c01d1eae907d50ac116(
    branch: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff9fa5a15e686d115ee6fc23bb85d6942edfd12793e7d8cdfb51b12c7bd91d58(
    git_repo_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__457187e968eb632c4dc3501b812b4f38e0dbe9a0ba3ce22b6deca7c3e3f550ea(
    vpc_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49a1de8fe00c26dbdd5f0353f96b074e2154998cb331e299fb76a9a1a2bc4919(
    p: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cec20d71b6e66d417a7cbbf29f4582feb6048ded9c9a511d16e02645e8bed25(
    project_description: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47c7b8991f69deb3dce291d9511e8c90ad87a5c51470a6a7dc10efb61019d78f(
    project_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d751bc8805262cceaff1945b81da131bd1b279a3e8970c0bfffcaa08d1a9518(
    event: GitEvent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70a2d54e99153d760066833565fc99621b594db93de0feeee3bd192a25a7cd90(
    schedule: _aws_cdk_aws_events_ceddda9d.Schedule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__371ef1a2fffc32327bc9a3d0ae0bb69ceb73341de5c1a9bc545eb466594723b5(
    branches: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab7d624c4b17ae5798d2698454d6664a420296e02d5be3d3594785bdcecf3128(
    name: builtins.str,
    *suffixes: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2992ae92902d8b81668ae7355ad4ea4ac8db2b07a12cd50a42be7f9e50929264(
    str: builtins.str,
    s: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__350c5bb98e107eee6ee21ce2e7e012972cbae0b757a37bd6ee1f5e66025eec9c(
    value: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0e4526132686dd17a76cbc5266bbd91f6ff16cdccfd3fd6245f1061a6ff514d(
    str: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a691b7ad10e5308aff51aa2082dc54b2a1b1cc77ade0cae68b1ecf78fba856a(
    url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e64ebb7228e613203bd98f40a1ff8cfe6b40703167a883bb3f0a0c727a79d2e7(
    stack: _aws_cdk_ceddda9d.Stack,
    persist: typing.Optional[builtins.bool] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4503a468a48cac5f6781501429a0ca70194cff93e94a9f9c1b72e64161ff096f(
    str: builtins.str,
    s: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2d5b06f249e7a0f41e6e205451860c1add18aeaa6bef4e833f655e2b1694860(
    scope: _constructs_77d1e7e8.IConstruct,
    rule_id: builtins.str,
    reason: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8335787277838180e459986b4f0f134fb3f147e37b0038a91887173bd63c7ecc(
    str: builtins.str,
    delimiter: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
