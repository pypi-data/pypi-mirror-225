'''
The static-website module is able to deploy your pre-packaged static website content into an S3 Bucket, fronted by Cloudfront. This module uses an Origin Access Identity to ensure your Bucket can only be accessed via Cloudfront and is configured to only allow HTTPS requests by default. Custom runtime configurations can also be specified which will emit a runtime-config.json file along with your website content. Typically this includes resource Arns, Id's etc which may need to be referenced from your website. This package uses sane defaults and at a minimum only requires the path to your website assets.

Below is a conceptual view of the default architecture this module creates:

```
Cloudfront Distribution (HTTPS only) -> S3 Bucket (Private via OAI)
|_ WAF V2 ACL                                |_ index.html (+ other website files and assets)
                                             |_ runtime-config.json
```

A typical use case is to create a static website with AuthN. To accomplish this, we can leverage the UserIdentity to create the User Pool (Cognito by default) and Identity Pool. We can then pipe the respective pool id's as runtimeOptions into the StaticWebsite. After the website is deployed, these values can be interrogated from the runtime-config.json deployed alongside the website in order to perform authentication within the app using something like the [Amplify Auth API](https://docs.amplify.aws/lib/client-configuration/configuring-amplify-categories/q/platform/js/#authentication-amazon-cognito).

```python
const userIdentity = new UserIdentity(this, 'UserIdentity');
new StaticWebsite(this, 'StaticWebsite', {
    websiteContentPath: '<relative>/<path>/<to>/<built>/<website>',
    runtimeOptions: {
        jsonPayload: {
            region: Stack.of(this).region,
            identityPoolId: userIdentity.identityPool.identityPoolId,
            userPoolId: userIdentity.userPool?.userPoolId,
            userPoolWebClientId: userIdentity.userPoolClient?.userPoolClientId,
        }
    },
});
```
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
import aws_cdk.aws_cloudfront as _aws_cdk_aws_cloudfront_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import aws_cdk.aws_s3_deployment as _aws_cdk_aws_s3_deployment_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/static-website.BucketDeploymentProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_control": "accessControl",
        "cache_control": "cacheControl",
        "content_disposition": "contentDisposition",
        "content_encoding": "contentEncoding",
        "content_language": "contentLanguage",
        "content_type": "contentType",
        "destination_key_prefix": "destinationKeyPrefix",
        "distribution": "distribution",
        "distribution_paths": "distributionPaths",
        "ephemeral_storage_size": "ephemeralStorageSize",
        "exclude": "exclude",
        "expires": "expires",
        "extract": "extract",
        "include": "include",
        "log_retention": "logRetention",
        "memory_limit": "memoryLimit",
        "metadata": "metadata",
        "prune": "prune",
        "retain_on_delete": "retainOnDelete",
        "role": "role",
        "server_side_encryption": "serverSideEncryption",
        "server_side_encryption_aws_kms_key_id": "serverSideEncryptionAwsKmsKeyId",
        "server_side_encryption_customer_algorithm": "serverSideEncryptionCustomerAlgorithm",
        "sign_content": "signContent",
        "storage_class": "storageClass",
        "use_efs": "useEfs",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
        "website_redirect_location": "websiteRedirectLocation",
    },
)
class BucketDeploymentProps:
    def __init__(
        self,
        *,
        access_control: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketAccessControl] = None,
        cache_control: typing.Optional[typing.Sequence[_aws_cdk_aws_s3_deployment_ceddda9d.CacheControl]] = None,
        content_disposition: typing.Optional[builtins.str] = None,
        content_encoding: typing.Optional[builtins.str] = None,
        content_language: typing.Optional[builtins.str] = None,
        content_type: typing.Optional[builtins.str] = None,
        destination_key_prefix: typing.Optional[builtins.str] = None,
        distribution: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IDistribution] = None,
        distribution_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        ephemeral_storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        expires: typing.Optional[_aws_cdk_ceddda9d.Expiration] = None,
        extract: typing.Optional[builtins.bool] = None,
        include: typing.Optional[typing.Sequence[builtins.str]] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        memory_limit: typing.Optional[jsii.Number] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        prune: typing.Optional[builtins.bool] = None,
        retain_on_delete: typing.Optional[builtins.bool] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        server_side_encryption: typing.Optional[_aws_cdk_aws_s3_deployment_ceddda9d.ServerSideEncryption] = None,
        server_side_encryption_aws_kms_key_id: typing.Optional[builtins.str] = None,
        server_side_encryption_customer_algorithm: typing.Optional[builtins.str] = None,
        sign_content: typing.Optional[builtins.bool] = None,
        storage_class: typing.Optional[_aws_cdk_aws_s3_deployment_ceddda9d.StorageClass] = None,
        use_efs: typing.Optional[builtins.bool] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        website_redirect_location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Bucket Deployment props.

        NOTE: forked from aws-cdk-lib/s3-deployment without any required props.

        :param access_control: (experimental) System-defined x-amz-acl metadata to be set on all objects in the deployment. Default: - Not set.
        :param cache_control: (experimental) System-defined cache-control metadata to be set on all objects in the deployment. Default: - Not set.
        :param content_disposition: (experimental) System-defined cache-disposition metadata to be set on all objects in the deployment. Default: - Not set.
        :param content_encoding: (experimental) System-defined content-encoding metadata to be set on all objects in the deployment. Default: - Not set.
        :param content_language: (experimental) System-defined content-language metadata to be set on all objects in the deployment. Default: - Not set.
        :param content_type: (experimental) System-defined content-type metadata to be set on all objects in the deployment. Default: - Not set.
        :param destination_key_prefix: (experimental) Key prefix in the destination bucket. Must be <=104 characters Default: "/" (unzip to root of the destination bucket)
        :param distribution: (experimental) The CloudFront distribution using the destination bucket as an origin. Files in the distribution's edge caches will be invalidated after files are uploaded to the destination bucket. Default: - No invalidation occurs
        :param distribution_paths: (experimental) The file paths to invalidate in the CloudFront distribution. Default: - All files under the destination bucket key prefix will be invalidated.
        :param ephemeral_storage_size: (experimental) The size of the AWS Lambda function’s /tmp directory in MiB. Default: 512 MiB
        :param exclude: (experimental) If this is set, matching files or objects will be excluded from the deployment's sync command. This can be used to exclude a file from being pruned in the destination bucket. If you want to just exclude files from the deployment package (which excludes these files evaluated when invalidating the asset), you should leverage the ``exclude`` property of ``AssetOptions`` when defining your source. Default: - No exclude filters are used
        :param expires: (experimental) System-defined expires metadata to be set on all objects in the deployment. Default: - The objects in the distribution will not expire.
        :param extract: (experimental) If this is set, the zip file will be synced to the destination S3 bucket and extracted. If false, the file will remain zipped in the destination bucket. Default: true
        :param include: (experimental) If this is set, matching files or objects will be included with the deployment's sync command. Since all files from the deployment package are included by default, this property is usually leveraged alongside an ``exclude`` filter. Default: - No include filters are used and all files are included with the sync command
        :param log_retention: (experimental) The number of days that the lambda function's log events are kept in CloudWatch Logs. Default: logs.RetentionDays.INFINITE
        :param memory_limit: (experimental) The amount of memory (in MiB) to allocate to the AWS Lambda function which replicates the files from the CDK bucket to the destination bucket. If you are deploying large files, you will need to increase this number accordingly. Default: 128
        :param metadata: (experimental) User-defined object metadata to be set on all objects in the deployment. Default: - No user metadata is set
        :param prune: (experimental) If this is set to false, files in the destination bucket that do not exist in the asset, will NOT be deleted during deployment (create/update). Default: true
        :param retain_on_delete: (experimental) If this is set to "false", the destination files will be deleted when the resource is deleted or the destination is updated. NOTICE: Configuring this to "false" might have operational implications. Please visit to the package documentation referred below to make sure you fully understand those implications. Default: true - when resource is deleted/updated, files are retained
        :param role: (experimental) Execution role associated with this function. Default: - A role is automatically created
        :param server_side_encryption: (experimental) System-defined x-amz-server-side-encryption metadata to be set on all objects in the deployment. Default: - Server side encryption is not used.
        :param server_side_encryption_aws_kms_key_id: (experimental) System-defined x-amz-server-side-encryption-aws-kms-key-id metadata to be set on all objects in the deployment. Default: - Not set.
        :param server_side_encryption_customer_algorithm: (experimental) System-defined x-amz-server-side-encryption-customer-algorithm metadata to be set on all objects in the deployment. Warning: This is not a useful parameter until this bug is fixed: https://github.com/aws/aws-cdk/issues/6080 Default: - Not set.
        :param sign_content: (experimental) If set to true, uploads will precompute the value of ``x-amz-content-sha256`` and include it in the signed S3 request headers. Default: - ``x-amz-content-sha256`` will not be computed
        :param storage_class: (experimental) System-defined x-amz-storage-class metadata to be set on all objects in the deployment. Default: - Default storage-class for the bucket is used.
        :param use_efs: (experimental) Mount an EFS file system. Enable this if your assets are large and you encounter disk space errors. Enabling this option will require a VPC to be specified. Default: - No EFS. Lambda has access only to 512MB of disk space.
        :param vpc: (experimental) The VPC network to place the deployment lambda handler in. This is required if ``useEfs`` is set. Default: None
        :param vpc_subnets: (experimental) Where in the VPC to place the deployment lambda handler. Only used if 'vpc' is supplied. Default: - the Vpc default strategy if not specified
        :param website_redirect_location: (experimental) System-defined x-amz-website-redirect-location metadata to be set on all objects in the deployment. Default: - No website redirection.

        :stability: experimental
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd638473174822cab7e3d3dc7883ae8792045c72ae3daa634c35c6f311a51d80)
            check_type(argname="argument access_control", value=access_control, expected_type=type_hints["access_control"])
            check_type(argname="argument cache_control", value=cache_control, expected_type=type_hints["cache_control"])
            check_type(argname="argument content_disposition", value=content_disposition, expected_type=type_hints["content_disposition"])
            check_type(argname="argument content_encoding", value=content_encoding, expected_type=type_hints["content_encoding"])
            check_type(argname="argument content_language", value=content_language, expected_type=type_hints["content_language"])
            check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
            check_type(argname="argument destination_key_prefix", value=destination_key_prefix, expected_type=type_hints["destination_key_prefix"])
            check_type(argname="argument distribution", value=distribution, expected_type=type_hints["distribution"])
            check_type(argname="argument distribution_paths", value=distribution_paths, expected_type=type_hints["distribution_paths"])
            check_type(argname="argument ephemeral_storage_size", value=ephemeral_storage_size, expected_type=type_hints["ephemeral_storage_size"])
            check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
            check_type(argname="argument expires", value=expires, expected_type=type_hints["expires"])
            check_type(argname="argument extract", value=extract, expected_type=type_hints["extract"])
            check_type(argname="argument include", value=include, expected_type=type_hints["include"])
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
            check_type(argname="argument memory_limit", value=memory_limit, expected_type=type_hints["memory_limit"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument prune", value=prune, expected_type=type_hints["prune"])
            check_type(argname="argument retain_on_delete", value=retain_on_delete, expected_type=type_hints["retain_on_delete"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument server_side_encryption", value=server_side_encryption, expected_type=type_hints["server_side_encryption"])
            check_type(argname="argument server_side_encryption_aws_kms_key_id", value=server_side_encryption_aws_kms_key_id, expected_type=type_hints["server_side_encryption_aws_kms_key_id"])
            check_type(argname="argument server_side_encryption_customer_algorithm", value=server_side_encryption_customer_algorithm, expected_type=type_hints["server_side_encryption_customer_algorithm"])
            check_type(argname="argument sign_content", value=sign_content, expected_type=type_hints["sign_content"])
            check_type(argname="argument storage_class", value=storage_class, expected_type=type_hints["storage_class"])
            check_type(argname="argument use_efs", value=use_efs, expected_type=type_hints["use_efs"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
            check_type(argname="argument website_redirect_location", value=website_redirect_location, expected_type=type_hints["website_redirect_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_control is not None:
            self._values["access_control"] = access_control
        if cache_control is not None:
            self._values["cache_control"] = cache_control
        if content_disposition is not None:
            self._values["content_disposition"] = content_disposition
        if content_encoding is not None:
            self._values["content_encoding"] = content_encoding
        if content_language is not None:
            self._values["content_language"] = content_language
        if content_type is not None:
            self._values["content_type"] = content_type
        if destination_key_prefix is not None:
            self._values["destination_key_prefix"] = destination_key_prefix
        if distribution is not None:
            self._values["distribution"] = distribution
        if distribution_paths is not None:
            self._values["distribution_paths"] = distribution_paths
        if ephemeral_storage_size is not None:
            self._values["ephemeral_storage_size"] = ephemeral_storage_size
        if exclude is not None:
            self._values["exclude"] = exclude
        if expires is not None:
            self._values["expires"] = expires
        if extract is not None:
            self._values["extract"] = extract
        if include is not None:
            self._values["include"] = include
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if memory_limit is not None:
            self._values["memory_limit"] = memory_limit
        if metadata is not None:
            self._values["metadata"] = metadata
        if prune is not None:
            self._values["prune"] = prune
        if retain_on_delete is not None:
            self._values["retain_on_delete"] = retain_on_delete
        if role is not None:
            self._values["role"] = role
        if server_side_encryption is not None:
            self._values["server_side_encryption"] = server_side_encryption
        if server_side_encryption_aws_kms_key_id is not None:
            self._values["server_side_encryption_aws_kms_key_id"] = server_side_encryption_aws_kms_key_id
        if server_side_encryption_customer_algorithm is not None:
            self._values["server_side_encryption_customer_algorithm"] = server_side_encryption_customer_algorithm
        if sign_content is not None:
            self._values["sign_content"] = sign_content
        if storage_class is not None:
            self._values["storage_class"] = storage_class
        if use_efs is not None:
            self._values["use_efs"] = use_efs
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if website_redirect_location is not None:
            self._values["website_redirect_location"] = website_redirect_location

    @builtins.property
    def access_control(
        self,
    ) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketAccessControl]:
        '''(experimental) System-defined x-amz-acl metadata to be set on all objects in the deployment.

        :default: - Not set.

        :see: https://docs.aws.amazon.com/AmazonS3/latest/userguide/acl-overview.html#canned-acl
        :stability: experimental
        '''
        result = self._values.get("access_control")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketAccessControl], result)

    @builtins.property
    def cache_control(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_s3_deployment_ceddda9d.CacheControl]]:
        '''(experimental) System-defined cache-control metadata to be set on all objects in the deployment.

        :default: - Not set.

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        :stability: experimental
        '''
        result = self._values.get("cache_control")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_s3_deployment_ceddda9d.CacheControl]], result)

    @builtins.property
    def content_disposition(self) -> typing.Optional[builtins.str]:
        '''(experimental) System-defined cache-disposition metadata to be set on all objects in the deployment.

        :default: - Not set.

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        :stability: experimental
        '''
        result = self._values.get("content_disposition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_encoding(self) -> typing.Optional[builtins.str]:
        '''(experimental) System-defined content-encoding metadata to be set on all objects in the deployment.

        :default: - Not set.

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        :stability: experimental
        '''
        result = self._values.get("content_encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_language(self) -> typing.Optional[builtins.str]:
        '''(experimental) System-defined content-language metadata to be set on all objects in the deployment.

        :default: - Not set.

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        :stability: experimental
        '''
        result = self._values.get("content_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_type(self) -> typing.Optional[builtins.str]:
        '''(experimental) System-defined content-type metadata to be set on all objects in the deployment.

        :default: - Not set.

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        :stability: experimental
        '''
        result = self._values.get("content_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_key_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) Key prefix in the destination bucket.

        Must be <=104 characters

        :default: "/" (unzip to root of the destination bucket)

        :stability: experimental
        '''
        result = self._values.get("destination_key_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def distribution(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IDistribution]:
        '''(experimental) The CloudFront distribution using the destination bucket as an origin.

        Files in the distribution's edge caches will be invalidated after
        files are uploaded to the destination bucket.

        :default: - No invalidation occurs

        :stability: experimental
        '''
        result = self._values.get("distribution")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IDistribution], result)

    @builtins.property
    def distribution_paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The file paths to invalidate in the CloudFront distribution.

        :default: - All files under the destination bucket key prefix will be invalidated.

        :stability: experimental
        '''
        result = self._values.get("distribution_paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ephemeral_storage_size(self) -> typing.Optional[_aws_cdk_ceddda9d.Size]:
        '''(experimental) The size of the AWS Lambda function’s /tmp directory in MiB.

        :default: 512 MiB

        :stability: experimental
        '''
        result = self._values.get("ephemeral_storage_size")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Size], result)

    @builtins.property
    def exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) If this is set, matching files or objects will be excluded from the deployment's sync command.

        This can be used to exclude a file from being pruned in the destination bucket.

        If you want to just exclude files from the deployment package (which excludes these files
        evaluated when invalidating the asset), you should leverage the ``exclude`` property of
        ``AssetOptions`` when defining your source.

        :default: - No exclude filters are used

        :see: https://docs.aws.amazon.com/cli/latest/reference/s3/index.html#use-of-exclude-and-include-filters
        :stability: experimental
        '''
        result = self._values.get("exclude")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def expires(self) -> typing.Optional[_aws_cdk_ceddda9d.Expiration]:
        '''(experimental) System-defined expires metadata to be set on all objects in the deployment.

        :default: - The objects in the distribution will not expire.

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        :stability: experimental
        '''
        result = self._values.get("expires")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Expiration], result)

    @builtins.property
    def extract(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If this is set, the zip file will be synced to the destination S3 bucket and extracted.

        If false, the file will remain zipped in the destination bucket.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("extract")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def include(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) If this is set, matching files or objects will be included with the deployment's sync command.

        Since all files from the deployment package are included by default, this property
        is usually leveraged alongside an ``exclude`` filter.

        :default: - No include filters are used and all files are included with the sync command

        :see: https://docs.aws.amazon.com/cli/latest/reference/s3/index.html#use-of-exclude-and-include-filters
        :stability: experimental
        '''
        result = self._values.get("include")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def log_retention(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays]:
        '''(experimental) The number of days that the lambda function's log events are kept in CloudWatch Logs.

        :default: logs.RetentionDays.INFINITE

        :stability: experimental
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays], result)

    @builtins.property
    def memory_limit(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The amount of memory (in MiB) to allocate to the AWS Lambda function which replicates the files from the CDK bucket to the destination bucket.

        If you are deploying large files, you will need to increase this number
        accordingly.

        :default: 128

        :stability: experimental
        '''
        result = self._values.get("memory_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) User-defined object metadata to be set on all objects in the deployment.

        :default: - No user metadata is set

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#UserMetadata
        :stability: experimental
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def prune(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If this is set to false, files in the destination bucket that do not exist in the asset, will NOT be deleted during deployment (create/update).

        :default: true

        :see: https://docs.aws.amazon.com/cli/latest/reference/s3/sync.html
        :stability: experimental
        '''
        result = self._values.get("prune")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def retain_on_delete(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If this is set to "false", the destination files will be deleted when the resource is deleted or the destination is updated.

        NOTICE: Configuring this to "false" might have operational implications. Please
        visit to the package documentation referred below to make sure you fully understand those implications.

        :default: true - when resource is deleted/updated, files are retained

        :see: https://github.com/aws/aws-cdk/tree/main/packages/%40aws-cdk/aws-s3-deployment#retain-on-delete
        :stability: experimental
        '''
        result = self._values.get("retain_on_delete")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) Execution role associated with this function.

        :default: - A role is automatically created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def server_side_encryption(
        self,
    ) -> typing.Optional[_aws_cdk_aws_s3_deployment_ceddda9d.ServerSideEncryption]:
        '''(experimental) System-defined x-amz-server-side-encryption metadata to be set on all objects in the deployment.

        :default: - Server side encryption is not used.

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        :stability: experimental
        '''
        result = self._values.get("server_side_encryption")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_deployment_ceddda9d.ServerSideEncryption], result)

    @builtins.property
    def server_side_encryption_aws_kms_key_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) System-defined x-amz-server-side-encryption-aws-kms-key-id metadata to be set on all objects in the deployment.

        :default: - Not set.

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        :stability: experimental
        '''
        result = self._values.get("server_side_encryption_aws_kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_side_encryption_customer_algorithm(
        self,
    ) -> typing.Optional[builtins.str]:
        '''(experimental) System-defined x-amz-server-side-encryption-customer-algorithm metadata to be set on all objects in the deployment.

        Warning: This is not a useful parameter until this bug is fixed: https://github.com/aws/aws-cdk/issues/6080

        :default: - Not set.

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/ServerSideEncryptionCustomerKeys.html#sse-c-how-to-programmatically-intro
        :stability: experimental
        '''
        result = self._values.get("server_side_encryption_customer_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sign_content(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If set to true, uploads will precompute the value of ``x-amz-content-sha256`` and include it in the signed S3 request headers.

        :default: - ``x-amz-content-sha256`` will not be computed

        :stability: experimental
        '''
        result = self._values.get("sign_content")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def storage_class(
        self,
    ) -> typing.Optional[_aws_cdk_aws_s3_deployment_ceddda9d.StorageClass]:
        '''(experimental) System-defined x-amz-storage-class metadata to be set on all objects in the deployment.

        :default: - Default storage-class for the bucket is used.

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        :stability: experimental
        '''
        result = self._values.get("storage_class")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_deployment_ceddda9d.StorageClass], result)

    @builtins.property
    def use_efs(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Mount an EFS file system.

        Enable this if your assets are large and you encounter disk space errors.
        Enabling this option will require a VPC to be specified.

        :default: - No EFS. Lambda has access only to 512MB of disk space.

        :stability: experimental
        '''
        result = self._values.get("use_efs")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''(experimental) The VPC network to place the deployment lambda handler in.

        This is required if ``useEfs`` is set.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''(experimental) Where in the VPC to place the deployment lambda handler.

        Only used if 'vpc' is supplied.

        :default: - the Vpc default strategy if not specified

        :stability: experimental
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def website_redirect_location(self) -> typing.Optional[builtins.str]:
        '''(experimental) System-defined x-amz-website-redirect-location metadata to be set on all objects in the deployment.

        :default: - No website redirection.

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        :stability: experimental
        '''
        result = self._values.get("website_redirect_location")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BucketDeploymentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/static-website.CidrAllowList",
    jsii_struct_bases=[],
    name_mapping={"cidr_ranges": "cidrRanges", "cidr_type": "cidrType"},
)
class CidrAllowList:
    def __init__(
        self,
        *,
        cidr_ranges: typing.Sequence[builtins.str],
        cidr_type: builtins.str,
    ) -> None:
        '''(experimental) Representation of a CIDR range.

        :param cidr_ranges: (experimental) Specify an IPv4 address by using CIDR notation. For example: To configure AWS WAF to allow, block, or count requests that originated from the IP address 192.0.2.44, specify 192.0.2.44/32 . To configure AWS WAF to allow, block, or count requests that originated from IP addresses from 192.0.2.0 to 192.0.2.255, specify 192.0.2.0/24 . For more information about CIDR notation, see the Wikipedia entry Classless Inter-Domain Routing . Specify an IPv6 address by using CIDR notation. For example: To configure AWS WAF to allow, block, or count requests that originated from the IP address 1111:0000:0000:0000:0000:0000:0000:0111, specify 1111:0000:0000:0000:0000:0000:0000:0111/128 . To configure AWS WAF to allow, block, or count requests that originated from IP addresses 1111:0000:0000:0000:0000:0000:0000:0000 to 1111:0000:0000:0000:ffff:ffff:ffff:ffff, specify 1111:0000:0000:0000:0000:0000:0000:0000/64 .
        :param cidr_type: (experimental) Type of CIDR range.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9be1ae061cd271ea75f6ed9932a2ad208594eb9b8cae56fd44d609778e3aa1fc)
            check_type(argname="argument cidr_ranges", value=cidr_ranges, expected_type=type_hints["cidr_ranges"])
            check_type(argname="argument cidr_type", value=cidr_type, expected_type=type_hints["cidr_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cidr_ranges": cidr_ranges,
            "cidr_type": cidr_type,
        }

    @builtins.property
    def cidr_ranges(self) -> typing.List[builtins.str]:
        '''(experimental) Specify an IPv4 address by using CIDR notation.

        For example:
        To configure AWS WAF to allow, block, or count requests that originated from the IP address 192.0.2.44, specify 192.0.2.44/32 .
        To configure AWS WAF to allow, block, or count requests that originated from IP addresses from 192.0.2.0 to 192.0.2.255, specify 192.0.2.0/24 .

        For more information about CIDR notation, see the Wikipedia entry Classless Inter-Domain Routing .

        Specify an IPv6 address by using CIDR notation. For example:
        To configure AWS WAF to allow, block, or count requests that originated from the IP address 1111:0000:0000:0000:0000:0000:0000:0111, specify 1111:0000:0000:0000:0000:0000:0000:0111/128 .
        To configure AWS WAF to allow, block, or count requests that originated from IP addresses 1111:0000:0000:0000:0000:0000:0000:0000 to 1111:0000:0000:0000:ffff:ffff:ffff:ffff, specify 1111:0000:0000:0000:0000:0000:0000:0000/64 .

        :stability: experimental
        '''
        result = self._values.get("cidr_ranges")
        assert result is not None, "Required property 'cidr_ranges' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def cidr_type(self) -> builtins.str:
        '''(experimental) Type of CIDR range.

        :stability: experimental
        '''
        result = self._values.get("cidr_type")
        assert result is not None, "Required property 'cidr_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CidrAllowList(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/static-website.CloudFrontWebAclProps",
    jsii_struct_bases=[],
    name_mapping={
        "cidr_allow_list": "cidrAllowList",
        "disable": "disable",
        "managed_rules": "managedRules",
    },
)
class CloudFrontWebAclProps:
    def __init__(
        self,
        *,
        cidr_allow_list: typing.Optional[typing.Union[CidrAllowList, typing.Dict[builtins.str, typing.Any]]] = None,
        disable: typing.Optional[builtins.bool] = None,
        managed_rules: typing.Optional[typing.Sequence[typing.Union["ManagedRule", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Properties to configure the web acl.

        :param cidr_allow_list: (experimental) List of cidr ranges to allow. Default: - undefined
        :param disable: (experimental) Set to true to prevent creation of a web acl for the static website. Default: false
        :param managed_rules: (experimental) List of managed rules to apply to the web acl. Default: - [{ vendor: "AWS", name: "AWSManagedRulesCommonRuleSet" }]

        :stability: experimental
        '''
        if isinstance(cidr_allow_list, dict):
            cidr_allow_list = CidrAllowList(**cidr_allow_list)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef5772598b3c7d231378f10846d94f00acdb7a6a00c290902b0f3d6fb2917a2a)
            check_type(argname="argument cidr_allow_list", value=cidr_allow_list, expected_type=type_hints["cidr_allow_list"])
            check_type(argname="argument disable", value=disable, expected_type=type_hints["disable"])
            check_type(argname="argument managed_rules", value=managed_rules, expected_type=type_hints["managed_rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cidr_allow_list is not None:
            self._values["cidr_allow_list"] = cidr_allow_list
        if disable is not None:
            self._values["disable"] = disable
        if managed_rules is not None:
            self._values["managed_rules"] = managed_rules

    @builtins.property
    def cidr_allow_list(self) -> typing.Optional[CidrAllowList]:
        '''(experimental) List of cidr ranges to allow.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("cidr_allow_list")
        return typing.cast(typing.Optional[CidrAllowList], result)

    @builtins.property
    def disable(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Set to true to prevent creation of a web acl for the static website.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("disable")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def managed_rules(self) -> typing.Optional[typing.List["ManagedRule"]]:
        '''(experimental) List of managed rules to apply to the web acl.

        :default: - [{ vendor: "AWS", name: "AWSManagedRulesCommonRuleSet" }]

        :stability: experimental
        '''
        result = self._values.get("managed_rules")
        return typing.cast(typing.Optional[typing.List["ManagedRule"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudFrontWebAclProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontWebAcl(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-prototyping-sdk/static-website.CloudfrontWebAcl",
):
    '''(experimental) This construct creates a WAFv2 Web ACL for cloudfront in the us-east-1 region (required for cloudfront) no matter the region of the parent cdk stack.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cidr_allow_list: typing.Optional[typing.Union[CidrAllowList, typing.Dict[builtins.str, typing.Any]]] = None,
        disable: typing.Optional[builtins.bool] = None,
        managed_rules: typing.Optional[typing.Sequence[typing.Union["ManagedRule", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cidr_allow_list: (experimental) List of cidr ranges to allow. Default: - undefined
        :param disable: (experimental) Set to true to prevent creation of a web acl for the static website. Default: false
        :param managed_rules: (experimental) List of managed rules to apply to the web acl. Default: - [{ vendor: "AWS", name: "AWSManagedRulesCommonRuleSet" }]

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bda7210fc0eeabc7cb6886da0c5813d2d87516e184bb00f6c26a30a1603b2e01)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CloudFrontWebAclProps(
            cidr_allow_list=cidr_allow_list,
            disable=disable,
            managed_rules=managed_rules,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="webAclArn")
    def web_acl_arn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "webAclArn"))

    @builtins.property
    @jsii.member(jsii_name="webAclId")
    def web_acl_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "webAclId"))


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/static-website.ManagedRule",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "vendor": "vendor"},
)
class ManagedRule:
    def __init__(self, *, name: builtins.str, vendor: builtins.str) -> None:
        '''(experimental) Represents a WAF V2 managed rule.

        :param name: (experimental) The name of the managed rule group. You use this, along with the vendor name, to identify the rule group.
        :param vendor: (experimental) The name of the managed rule group vendor. You use this, along with the rule group name, to identify the rule group.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdd742c7cda95301b9d5bfd45ee16073ed1afed5d3d8dd45ade23d4ea343e9b8)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument vendor", value=vendor, expected_type=type_hints["vendor"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "vendor": vendor,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The name of the managed rule group.

        You use this, along with the vendor name, to identify the rule group.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vendor(self) -> builtins.str:
        '''(experimental) The name of the managed rule group vendor.

        You use this, along with the rule group name, to identify the rule group.

        :stability: experimental
        '''
        result = self._values.get("vendor")
        assert result is not None, "Required property 'vendor' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManagedRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/static-website.RuntimeOptions",
    jsii_struct_bases=[],
    name_mapping={"json_payload": "jsonPayload", "json_file_name": "jsonFileName"},
)
class RuntimeOptions:
    def __init__(
        self,
        *,
        json_payload: typing.Any,
        json_file_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Dynamic configuration which gets resolved only during deployment.

        :param json_payload: (experimental) Arbitrary JSON payload containing runtime values to deploy. Typically this contains resourceArns, etc which are only known at deploy time.
        :param json_file_name: (experimental) File name to store runtime configuration (jsonPayload). Must follow pattern: '*.json' Default: "runtime-config.json"

        :stability: experimental

        Example::

            // Will store a JSON file called runtime-config.json in the root of the StaticWebsite S3 bucket containing any
            // and all resolved values.
            const runtimeConfig = {jsonPayload: {bucketArn: s3Bucket.bucketArn}};
            new StaticWebsite(scope, 'StaticWebsite', {websiteContentPath: 'path/to/website', runtimeConfig});
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ad60143626012a4b255fa575178b1ba2bbe7a959037c2520d6cd003f7ee3cde)
            check_type(argname="argument json_payload", value=json_payload, expected_type=type_hints["json_payload"])
            check_type(argname="argument json_file_name", value=json_file_name, expected_type=type_hints["json_file_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "json_payload": json_payload,
        }
        if json_file_name is not None:
            self._values["json_file_name"] = json_file_name

    @builtins.property
    def json_payload(self) -> typing.Any:
        '''(experimental) Arbitrary JSON payload containing runtime values to deploy.

        Typically this contains resourceArns, etc which
        are only known at deploy time.

        :stability: experimental

        Example::

            { userPoolId: some.userPool.userPoolId, someResourceArn: some.resource.Arn }
        '''
        result = self._values.get("json_payload")
        assert result is not None, "Required property 'json_payload' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def json_file_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) File name to store runtime configuration (jsonPayload).

        Must follow pattern: '*.json'

        :default: "runtime-config.json"

        :stability: experimental
        '''
        result = self._values.get("json_file_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RuntimeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StaticWebsite(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-prototyping-sdk/static-website.StaticWebsite",
):
    '''(experimental) Deploys a Static Website using by default a private S3 bucket as an origin and Cloudfront as the entrypoint.

    This construct configures a webAcl containing rules that are generally applicable to web applications. This
    provides protection against exploitation of a wide range of vulnerabilities, including some of the high risk
    and commonly occurring vulnerabilities described in OWASP publications such as OWASP Top 10.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        website_content_path: builtins.str,
        bucket_deployment_props: typing.Optional[typing.Union[BucketDeploymentProps, typing.Dict[builtins.str, typing.Any]]] = None,
        default_website_bucket_encryption: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketEncryption] = None,
        default_website_bucket_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key] = None,
        distribution_props: typing.Optional[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.DistributionProps, typing.Dict[builtins.str, typing.Any]]] = None,
        runtime_options: typing.Optional[typing.Union[RuntimeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        web_acl_props: typing.Optional[typing.Union[CloudFrontWebAclProps, typing.Dict[builtins.str, typing.Any]]] = None,
        website_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param website_content_path: (experimental) Path to the directory containing the static website files and assets. This directory must contain an index.html file.
        :param bucket_deployment_props: (experimental) Custom bucket deployment properties. Example::
        :param default_website_bucket_encryption: (experimental) Bucket encryption to use for the default bucket. Supported options are KMS or S3MANAGED. Note: If planning to use KMS, ensure you associate a Lambda Edge function to sign requests to S3 as OAI does not currently support KMS encryption. Refer to {@link https://aws.amazon.com/blogs/networking-and-content-delivery/serving-sse-kms-encrypted-content-from-s3-using-cloudfront/} Default: - "S3MANAGED"
        :param default_website_bucket_encryption_key: (experimental) A predefined KMS customer encryption key to use for the default bucket that gets created. Note: This is only used if the websiteBucket is left undefined, otherwise all settings from the provided websiteBucket will be used.
        :param distribution_props: (experimental) Custom distribution properties. Note: defaultBehaviour.origin is a required parameter, however it will not be used as this construct will wire it on your behalf. You will need to pass in an instance of StaticWebsiteOrigin (NoOp) to keep the compiler happy.
        :param runtime_options: (experimental) Dynamic configuration which gets resolved only during deployment.
        :param web_acl_props: (experimental) Limited configuration settings for the generated webAcl. For more advanced settings, create your own ACL and pass in the webAclId as a param to distributionProps. Note: If pass in your own ACL, make sure the SCOPE is CLOUDFRONT and it is created in us-east-1.
        :param website_bucket: (experimental) Predefined bucket to deploy the website into.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__928ab420af56897a7ec742ca8c51b67d3585108c8122ca2cabcbb563ad0078dc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = StaticWebsiteProps(
            website_content_path=website_content_path,
            bucket_deployment_props=bucket_deployment_props,
            default_website_bucket_encryption=default_website_bucket_encryption,
            default_website_bucket_encryption_key=default_website_bucket_encryption_key,
            distribution_props=distribution_props,
            runtime_options=runtime_options,
            web_acl_props=web_acl_props,
            website_bucket=website_bucket,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="bucketDeployment")
    def bucket_deployment(self) -> _aws_cdk_aws_s3_deployment_ceddda9d.BucketDeployment:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_s3_deployment_ceddda9d.BucketDeployment, jsii.get(self, "bucketDeployment"))

    @builtins.property
    @jsii.member(jsii_name="cloudFrontDistribution")
    def cloud_front_distribution(self) -> _aws_cdk_aws_cloudfront_ceddda9d.Distribution:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_cloudfront_ceddda9d.Distribution, jsii.get(self, "cloudFrontDistribution"))

    @builtins.property
    @jsii.member(jsii_name="websiteBucket")
    def website_bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, jsii.get(self, "websiteBucket"))


@jsii.implements(_aws_cdk_aws_cloudfront_ceddda9d.IOrigin)
class StaticWebsiteOrigin(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-prototyping-sdk/static-website.StaticWebsiteOrigin",
):
    '''(experimental) If passing in distributionProps, the default behaviour.origin is a required parameter. An instance of this class can be passed in to make the compiler happy.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _constructs_77d1e7e8.Construct,
        *,
        origin_id: builtins.str,
    ) -> _aws_cdk_aws_cloudfront_ceddda9d.OriginBindConfig:
        '''(experimental) The method called when a given Origin is added (for the first time) to a Distribution.

        :param _scope: -
        :param origin_id: The identifier of this Origin, as assigned by the Distribution this Origin has been used added to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__517101de23606077d92f012a8febe5855c5958495ee337733884797c5511261b)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        _options = _aws_cdk_aws_cloudfront_ceddda9d.OriginBindOptions(
            origin_id=origin_id
        )

        return typing.cast(_aws_cdk_aws_cloudfront_ceddda9d.OriginBindConfig, jsii.invoke(self, "bind", [_scope, _options]))


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/static-website.StaticWebsiteProps",
    jsii_struct_bases=[],
    name_mapping={
        "website_content_path": "websiteContentPath",
        "bucket_deployment_props": "bucketDeploymentProps",
        "default_website_bucket_encryption": "defaultWebsiteBucketEncryption",
        "default_website_bucket_encryption_key": "defaultWebsiteBucketEncryptionKey",
        "distribution_props": "distributionProps",
        "runtime_options": "runtimeOptions",
        "web_acl_props": "webAclProps",
        "website_bucket": "websiteBucket",
    },
)
class StaticWebsiteProps:
    def __init__(
        self,
        *,
        website_content_path: builtins.str,
        bucket_deployment_props: typing.Optional[typing.Union[BucketDeploymentProps, typing.Dict[builtins.str, typing.Any]]] = None,
        default_website_bucket_encryption: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketEncryption] = None,
        default_website_bucket_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key] = None,
        distribution_props: typing.Optional[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.DistributionProps, typing.Dict[builtins.str, typing.Any]]] = None,
        runtime_options: typing.Optional[typing.Union[RuntimeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        web_acl_props: typing.Optional[typing.Union[CloudFrontWebAclProps, typing.Dict[builtins.str, typing.Any]]] = None,
        website_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    ) -> None:
        '''(experimental) Properties for configuring the StaticWebsite.

        :param website_content_path: (experimental) Path to the directory containing the static website files and assets. This directory must contain an index.html file.
        :param bucket_deployment_props: (experimental) Custom bucket deployment properties. Example::
        :param default_website_bucket_encryption: (experimental) Bucket encryption to use for the default bucket. Supported options are KMS or S3MANAGED. Note: If planning to use KMS, ensure you associate a Lambda Edge function to sign requests to S3 as OAI does not currently support KMS encryption. Refer to {@link https://aws.amazon.com/blogs/networking-and-content-delivery/serving-sse-kms-encrypted-content-from-s3-using-cloudfront/} Default: - "S3MANAGED"
        :param default_website_bucket_encryption_key: (experimental) A predefined KMS customer encryption key to use for the default bucket that gets created. Note: This is only used if the websiteBucket is left undefined, otherwise all settings from the provided websiteBucket will be used.
        :param distribution_props: (experimental) Custom distribution properties. Note: defaultBehaviour.origin is a required parameter, however it will not be used as this construct will wire it on your behalf. You will need to pass in an instance of StaticWebsiteOrigin (NoOp) to keep the compiler happy.
        :param runtime_options: (experimental) Dynamic configuration which gets resolved only during deployment.
        :param web_acl_props: (experimental) Limited configuration settings for the generated webAcl. For more advanced settings, create your own ACL and pass in the webAclId as a param to distributionProps. Note: If pass in your own ACL, make sure the SCOPE is CLOUDFRONT and it is created in us-east-1.
        :param website_bucket: (experimental) Predefined bucket to deploy the website into.

        :stability: experimental
        '''
        if isinstance(bucket_deployment_props, dict):
            bucket_deployment_props = BucketDeploymentProps(**bucket_deployment_props)
        if isinstance(distribution_props, dict):
            distribution_props = _aws_cdk_aws_cloudfront_ceddda9d.DistributionProps(**distribution_props)
        if isinstance(runtime_options, dict):
            runtime_options = RuntimeOptions(**runtime_options)
        if isinstance(web_acl_props, dict):
            web_acl_props = CloudFrontWebAclProps(**web_acl_props)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89bfc04e26592eb60007e9b24484c68d1fa7dc22a410a69651d541193f397f08)
            check_type(argname="argument website_content_path", value=website_content_path, expected_type=type_hints["website_content_path"])
            check_type(argname="argument bucket_deployment_props", value=bucket_deployment_props, expected_type=type_hints["bucket_deployment_props"])
            check_type(argname="argument default_website_bucket_encryption", value=default_website_bucket_encryption, expected_type=type_hints["default_website_bucket_encryption"])
            check_type(argname="argument default_website_bucket_encryption_key", value=default_website_bucket_encryption_key, expected_type=type_hints["default_website_bucket_encryption_key"])
            check_type(argname="argument distribution_props", value=distribution_props, expected_type=type_hints["distribution_props"])
            check_type(argname="argument runtime_options", value=runtime_options, expected_type=type_hints["runtime_options"])
            check_type(argname="argument web_acl_props", value=web_acl_props, expected_type=type_hints["web_acl_props"])
            check_type(argname="argument website_bucket", value=website_bucket, expected_type=type_hints["website_bucket"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "website_content_path": website_content_path,
        }
        if bucket_deployment_props is not None:
            self._values["bucket_deployment_props"] = bucket_deployment_props
        if default_website_bucket_encryption is not None:
            self._values["default_website_bucket_encryption"] = default_website_bucket_encryption
        if default_website_bucket_encryption_key is not None:
            self._values["default_website_bucket_encryption_key"] = default_website_bucket_encryption_key
        if distribution_props is not None:
            self._values["distribution_props"] = distribution_props
        if runtime_options is not None:
            self._values["runtime_options"] = runtime_options
        if web_acl_props is not None:
            self._values["web_acl_props"] = web_acl_props
        if website_bucket is not None:
            self._values["website_bucket"] = website_bucket

    @builtins.property
    def website_content_path(self) -> builtins.str:
        '''(experimental) Path to the directory containing the static website files and assets.

        This directory must contain an index.html file.

        :stability: experimental
        '''
        result = self._values.get("website_content_path")
        assert result is not None, "Required property 'website_content_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bucket_deployment_props(self) -> typing.Optional[BucketDeploymentProps]:
        '''(experimental) Custom bucket deployment properties.

        Example::

        :stability: experimental
        '''
        result = self._values.get("bucket_deployment_props")
        return typing.cast(typing.Optional[BucketDeploymentProps], result)

    @builtins.property
    def default_website_bucket_encryption(
        self,
    ) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketEncryption]:
        '''(experimental) Bucket encryption to use for the default bucket.

        Supported options are KMS or S3MANAGED.

        Note: If planning to use KMS, ensure you associate a Lambda Edge function to sign requests to S3 as OAI does not currently support KMS encryption. Refer to {@link https://aws.amazon.com/blogs/networking-and-content-delivery/serving-sse-kms-encrypted-content-from-s3-using-cloudfront/}

        :default: - "S3MANAGED"

        :stability: experimental
        '''
        result = self._values.get("default_website_bucket_encryption")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketEncryption], result)

    @builtins.property
    def default_website_bucket_encryption_key(
        self,
    ) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key]:
        '''(experimental) A predefined KMS customer encryption key to use for the default bucket that gets created.

        Note: This is only used if the websiteBucket is left undefined, otherwise all settings from the provided websiteBucket will be used.

        :stability: experimental
        '''
        result = self._values.get("default_website_bucket_encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key], result)

    @builtins.property
    def distribution_props(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.DistributionProps]:
        '''(experimental) Custom distribution properties.

        Note: defaultBehaviour.origin is a required parameter, however it will not be used as this construct will wire it on your behalf.
        You will need to pass in an instance of StaticWebsiteOrigin (NoOp) to keep the compiler happy.

        :stability: experimental
        '''
        result = self._values.get("distribution_props")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.DistributionProps], result)

    @builtins.property
    def runtime_options(self) -> typing.Optional[RuntimeOptions]:
        '''(experimental) Dynamic configuration which gets resolved only during deployment.

        :stability: experimental
        '''
        result = self._values.get("runtime_options")
        return typing.cast(typing.Optional[RuntimeOptions], result)

    @builtins.property
    def web_acl_props(self) -> typing.Optional[CloudFrontWebAclProps]:
        '''(experimental) Limited configuration settings for the generated webAcl.

        For more advanced settings, create your own ACL and pass in the webAclId as a param to distributionProps.

        Note: If pass in your own ACL, make sure the SCOPE is CLOUDFRONT and it is created in us-east-1.

        :stability: experimental
        '''
        result = self._values.get("web_acl_props")
        return typing.cast(typing.Optional[CloudFrontWebAclProps], result)

    @builtins.property
    def website_bucket(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket]:
        '''(experimental) Predefined bucket to deploy the website into.

        :stability: experimental
        '''
        result = self._values.get("website_bucket")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StaticWebsiteProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "BucketDeploymentProps",
    "CidrAllowList",
    "CloudFrontWebAclProps",
    "CloudfrontWebAcl",
    "ManagedRule",
    "RuntimeOptions",
    "StaticWebsite",
    "StaticWebsiteOrigin",
    "StaticWebsiteProps",
]

publication.publish()

def _typecheckingstub__dd638473174822cab7e3d3dc7883ae8792045c72ae3daa634c35c6f311a51d80(
    *,
    access_control: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketAccessControl] = None,
    cache_control: typing.Optional[typing.Sequence[_aws_cdk_aws_s3_deployment_ceddda9d.CacheControl]] = None,
    content_disposition: typing.Optional[builtins.str] = None,
    content_encoding: typing.Optional[builtins.str] = None,
    content_language: typing.Optional[builtins.str] = None,
    content_type: typing.Optional[builtins.str] = None,
    destination_key_prefix: typing.Optional[builtins.str] = None,
    distribution: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IDistribution] = None,
    distribution_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    ephemeral_storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    expires: typing.Optional[_aws_cdk_ceddda9d.Expiration] = None,
    extract: typing.Optional[builtins.bool] = None,
    include: typing.Optional[typing.Sequence[builtins.str]] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    memory_limit: typing.Optional[jsii.Number] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    prune: typing.Optional[builtins.bool] = None,
    retain_on_delete: typing.Optional[builtins.bool] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    server_side_encryption: typing.Optional[_aws_cdk_aws_s3_deployment_ceddda9d.ServerSideEncryption] = None,
    server_side_encryption_aws_kms_key_id: typing.Optional[builtins.str] = None,
    server_side_encryption_customer_algorithm: typing.Optional[builtins.str] = None,
    sign_content: typing.Optional[builtins.bool] = None,
    storage_class: typing.Optional[_aws_cdk_aws_s3_deployment_ceddda9d.StorageClass] = None,
    use_efs: typing.Optional[builtins.bool] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    website_redirect_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9be1ae061cd271ea75f6ed9932a2ad208594eb9b8cae56fd44d609778e3aa1fc(
    *,
    cidr_ranges: typing.Sequence[builtins.str],
    cidr_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef5772598b3c7d231378f10846d94f00acdb7a6a00c290902b0f3d6fb2917a2a(
    *,
    cidr_allow_list: typing.Optional[typing.Union[CidrAllowList, typing.Dict[builtins.str, typing.Any]]] = None,
    disable: typing.Optional[builtins.bool] = None,
    managed_rules: typing.Optional[typing.Sequence[typing.Union[ManagedRule, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bda7210fc0eeabc7cb6886da0c5813d2d87516e184bb00f6c26a30a1603b2e01(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cidr_allow_list: typing.Optional[typing.Union[CidrAllowList, typing.Dict[builtins.str, typing.Any]]] = None,
    disable: typing.Optional[builtins.bool] = None,
    managed_rules: typing.Optional[typing.Sequence[typing.Union[ManagedRule, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdd742c7cda95301b9d5bfd45ee16073ed1afed5d3d8dd45ade23d4ea343e9b8(
    *,
    name: builtins.str,
    vendor: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ad60143626012a4b255fa575178b1ba2bbe7a959037c2520d6cd003f7ee3cde(
    *,
    json_payload: typing.Any,
    json_file_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__928ab420af56897a7ec742ca8c51b67d3585108c8122ca2cabcbb563ad0078dc(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    website_content_path: builtins.str,
    bucket_deployment_props: typing.Optional[typing.Union[BucketDeploymentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    default_website_bucket_encryption: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketEncryption] = None,
    default_website_bucket_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key] = None,
    distribution_props: typing.Optional[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.DistributionProps, typing.Dict[builtins.str, typing.Any]]] = None,
    runtime_options: typing.Optional[typing.Union[RuntimeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    web_acl_props: typing.Optional[typing.Union[CloudFrontWebAclProps, typing.Dict[builtins.str, typing.Any]]] = None,
    website_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__517101de23606077d92f012a8febe5855c5958495ee337733884797c5511261b(
    _scope: _constructs_77d1e7e8.Construct,
    *,
    origin_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89bfc04e26592eb60007e9b24484c68d1fa7dc22a410a69651d541193f397f08(
    *,
    website_content_path: builtins.str,
    bucket_deployment_props: typing.Optional[typing.Union[BucketDeploymentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    default_website_bucket_encryption: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketEncryption] = None,
    default_website_bucket_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key] = None,
    distribution_props: typing.Optional[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.DistributionProps, typing.Dict[builtins.str, typing.Any]]] = None,
    runtime_options: typing.Optional[typing.Union[RuntimeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    web_acl_props: typing.Optional[typing.Union[CloudFrontWebAclProps, typing.Dict[builtins.str, typing.Any]]] = None,
    website_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
) -> None:
    """Type checking stubs"""
    pass
