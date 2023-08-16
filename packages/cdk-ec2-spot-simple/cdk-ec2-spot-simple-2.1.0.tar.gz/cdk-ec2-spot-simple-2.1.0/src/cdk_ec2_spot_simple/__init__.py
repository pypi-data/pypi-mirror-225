'''
# cdk-ec2-spot-simple

[![npm](https://img.shields.io/npm/v/cdk-ec2-spot-simple)](https://www.npmjs.com/package/cdk-ec2-spot-simple)
[![PyPI](https://img.shields.io/pypi/v/cdk-ec2-spot-simple)](https://pypi.org/project/cdk-ec2-spot-simple)
[![Nuget](https://img.shields.io/nuget/v/TksSt.Cdk.Ec2SpotSimple)](https://www.nuget.org/packages/TksSt.Cdk.Ec2SpotSimple)
[![Maven Central](https://img.shields.io/maven-central/v/st.tks.cdk/ec2-spot-simple)](https://search.maven.org/artifact/st.tks.cdk/ec2-spot-simple)
[![View on Construct Hub](https://constructs.dev/badge?package=cdk-ec2-spot-simple)](https://constructs.dev/packages/cdk-ec2-spot-simple)

CDK construct library to create EC2 Spot Instances simply.

## Install

### TypeScript/JavaScript

```shell
npm install cdk-ec2-spot-simple
```

```shell
pnpm add cdk-ec2-spot-simple
```

```shell
yarn add cdk-ec2-spot-simple
```

### Python

```shell
pip install cdk-ec2-spot-simple
```

### .NET

```shell
dotnet add package TksSt.Cdk.Ec2SpotSimple
```

### Java

```xml
<dependency>
    <groupId>st.tks.cdk</groupId>
    <artifactId>ec2-spot-simple</artifactId>
</dependency>
```

### Go

```shell
go get github.com/tksst/cdk-ec2-spot-simple-go/cdkec2spotsimple/v2
```

## Usage

To set up a spot instance with default parameters, simply use "SpotInstance" instead of "ec2.Instance".

```python
import { SpotInstance } from "cdk-ec2-spot-simple"
import * as ec2 from "aws-cdk-lib/aws-ec2"

// Simple usage
new SpotInstance(this, "DefaultConfigSpotInstance", {
    // Required properties of "ec2.Instance"
    vpc: ec2.Vpc.fromLookup(this, "defaultVPC", { isDefault: true });,
    instanceType: ec2.InstanceType.of(ec2.InstanceClass.T3A, ec2.InstanceSize.NANO),
    machineImage: new ec2.AmazonLinuxImage(),
});

// Advanced usage
new SpotInstance(this, "StoppableSpotInstance", {
    // Required properties of "ec2.Instance"
    vpc: ec2.Vpc.fromLookup(this, "defaultVPC", { isDefault: true });,
    instanceType: ec2.InstanceType.of(ec2.InstanceClass.T3A, ec2.InstanceSize.NANO),
    machineImage: new ec2.AmazonLinuxImage(),
    // SpotInstance specific property
    spotOptions: {
        interruptionBehavior: ec2.SpotInstanceInterruption.STOP,
        requestType: ec2.SpotRequestType.PERSISTENT,
        maxPrice: 0.007,
    },
});
```

## API document

[See Construct Hub](https://constructs.dev/packages/cdk-ec2-spot-simple)

## Background

The `Instance` construct in `aws-cdk-lib/aws-ec2` does not have any spot instance functionality.

This `SpotInstance` construct creates `LaunchTemplate` that is enabled spot request internally and associate with `Instance`.

Also, `SpotInstance` creates a Lambda-backed custom resource if the spot requiest type is PERSISTENT. That resource deletes the spot request when the stack is destroyed.
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
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import constructs as _constructs_77d1e7e8


class SpotInstance(
    _aws_cdk_aws_ec2_ceddda9d.Instance,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-ec2-spot-simple.SpotInstance",
):
    '''This represents a single EC2 Spot instance and other necessary resources.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        spot_options: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.LaunchTemplateSpotOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        spot_req_canceler_options: typing.Optional[typing.Union["SpotReqCancelerProps", typing.Dict[builtins.str, typing.Any]]] = None,
        instance_type: _aws_cdk_aws_ec2_ceddda9d.InstanceType,
        machine_image: _aws_cdk_aws_ec2_ceddda9d.IMachineImage,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        allow_all_outbound: typing.Optional[builtins.bool] = None,
        availability_zone: typing.Optional[builtins.str] = None,
        block_devices: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.BlockDevice, typing.Dict[builtins.str, typing.Any]]]] = None,
        detailed_monitoring: typing.Optional[builtins.bool] = None,
        init: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.CloudFormationInit] = None,
        init_options: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.ApplyCloudFormationInitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        instance_name: typing.Optional[builtins.str] = None,
        key_name: typing.Optional[builtins.str] = None,
        private_ip_address: typing.Optional[builtins.str] = None,
        propagate_tags_to_volume_on_creation: typing.Optional[builtins.bool] = None,
        require_imdsv2: typing.Optional[builtins.bool] = None,
        resource_signal_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        source_dest_check: typing.Optional[builtins.bool] = None,
        user_data: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData] = None,
        user_data_causes_replacement: typing.Optional[builtins.bool] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param spot_options: The options for the Spot instances. Default: - Use the Launch Template's default InstanceMarketOptions.
        :param spot_req_canceler_options: Options related to Lambda functions to cancel spot requests.
        :param instance_type: Type of instance to launch.
        :param machine_image: AMI to launch.
        :param vpc: VPC to launch the instance in.
        :param allow_all_outbound: Whether the instance could initiate connections to anywhere by default. This property is only used when you do not provide a security group. Default: true
        :param availability_zone: In which AZ to place the instance within the VPC. Default: - Random zone.
        :param block_devices: Specifies how block devices are exposed to the instance. You can specify virtual devices and EBS volumes. Each instance that is launched has an associated root device volume, either an Amazon EBS volume or an instance store volume. You can use block device mappings to specify additional EBS volumes or instance store volumes to attach to an instance when it is launched. Default: - Uses the block device mapping of the AMI
        :param detailed_monitoring: Whether "Detailed Monitoring" is enabled for this instance Keep in mind that Detailed Monitoring results in extra charges. Default: - false
        :param init: Apply the given CloudFormation Init configuration to the instance at startup. Default: - no CloudFormation init
        :param init_options: Use the given options for applying CloudFormation Init. Describes the configsets to use and the timeout to wait Default: - default options
        :param instance_name: The name of the instance. Default: - CDK generated name
        :param key_name: Name of SSH keypair to grant access to instance. Default: - No SSH access will be possible.
        :param private_ip_address: Defines a private IP address to associate with an instance. Private IP should be available within the VPC that the instance is build within. Default: - no association
        :param propagate_tags_to_volume_on_creation: Propagate the EC2 instance tags to the EBS volumes. Default: - false
        :param require_imdsv2: Whether IMDSv2 should be required on this instance. Default: - false
        :param resource_signal_timeout: The length of time to wait for the resourceSignalCount. The maximum value is 43200 (12 hours). Default: Duration.minutes(5)
        :param role: An IAM role to associate with the instance profile assigned to this Auto Scaling Group. The role must be assumable by the service principal ``ec2.amazonaws.com``: Default: - A role will automatically be created, it can be accessed via the ``role`` property
        :param security_group: Security Group to assign to this instance. Default: - create new security group
        :param source_dest_check: Specifies whether to enable an instance launched in a VPC to perform NAT. This controls whether source/destination checking is enabled on the instance. A value of true means that checking is enabled, and false means that checking is disabled. The value must be false for the instance to perform NAT. Default: true
        :param user_data: Specific UserData to use. The UserData may still be mutated after creation. Default: - A UserData object appropriate for the MachineImage's Operating System is created.
        :param user_data_causes_replacement: Changes to the UserData force replacement. Depending the EC2 instance type, changing UserData either restarts the instance or replaces the instance. - Instance store-backed instances are replaced. - EBS-backed instances are restarted. By default, restarting does not execute the new UserData so you will need a different mechanism to ensure the instance is restarted. Setting this to ``true`` will make the instance's Logical ID depend on the UserData, which will cause CloudFormation to replace it if the UserData changes. Default: - true iff ``initOptions`` is specified, false otherwise.
        :param vpc_subnets: Where to place the instance within the VPC. Default: - Private subnets.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__051e0cc92650cdd834123f9ea5d7c961a30feed47306a6a346d2f06e3774662b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SpotInstanceProps(
            spot_options=spot_options,
            spot_req_canceler_options=spot_req_canceler_options,
            instance_type=instance_type,
            machine_image=machine_image,
            vpc=vpc,
            allow_all_outbound=allow_all_outbound,
            availability_zone=availability_zone,
            block_devices=block_devices,
            detailed_monitoring=detailed_monitoring,
            init=init,
            init_options=init_options,
            instance_name=instance_name,
            key_name=key_name,
            private_ip_address=private_ip_address,
            propagate_tags_to_volume_on_creation=propagate_tags_to_volume_on_creation,
            require_imdsv2=require_imdsv2,
            resource_signal_timeout=resource_signal_timeout,
            role=role,
            security_group=security_group,
            source_dest_check=source_dest_check,
            user_data=user_data,
            user_data_causes_replacement=user_data_causes_replacement,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-ec2-spot-simple.SpotInstanceProps",
    jsii_struct_bases=[_aws_cdk_aws_ec2_ceddda9d.InstanceProps],
    name_mapping={
        "instance_type": "instanceType",
        "machine_image": "machineImage",
        "vpc": "vpc",
        "allow_all_outbound": "allowAllOutbound",
        "availability_zone": "availabilityZone",
        "block_devices": "blockDevices",
        "detailed_monitoring": "detailedMonitoring",
        "init": "init",
        "init_options": "initOptions",
        "instance_name": "instanceName",
        "key_name": "keyName",
        "private_ip_address": "privateIpAddress",
        "propagate_tags_to_volume_on_creation": "propagateTagsToVolumeOnCreation",
        "require_imdsv2": "requireImdsv2",
        "resource_signal_timeout": "resourceSignalTimeout",
        "role": "role",
        "security_group": "securityGroup",
        "source_dest_check": "sourceDestCheck",
        "user_data": "userData",
        "user_data_causes_replacement": "userDataCausesReplacement",
        "vpc_subnets": "vpcSubnets",
        "spot_options": "spotOptions",
        "spot_req_canceler_options": "spotReqCancelerOptions",
    },
)
class SpotInstanceProps(_aws_cdk_aws_ec2_ceddda9d.InstanceProps):
    def __init__(
        self,
        *,
        instance_type: _aws_cdk_aws_ec2_ceddda9d.InstanceType,
        machine_image: _aws_cdk_aws_ec2_ceddda9d.IMachineImage,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        allow_all_outbound: typing.Optional[builtins.bool] = None,
        availability_zone: typing.Optional[builtins.str] = None,
        block_devices: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.BlockDevice, typing.Dict[builtins.str, typing.Any]]]] = None,
        detailed_monitoring: typing.Optional[builtins.bool] = None,
        init: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.CloudFormationInit] = None,
        init_options: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.ApplyCloudFormationInitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        instance_name: typing.Optional[builtins.str] = None,
        key_name: typing.Optional[builtins.str] = None,
        private_ip_address: typing.Optional[builtins.str] = None,
        propagate_tags_to_volume_on_creation: typing.Optional[builtins.bool] = None,
        require_imdsv2: typing.Optional[builtins.bool] = None,
        resource_signal_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        source_dest_check: typing.Optional[builtins.bool] = None,
        user_data: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData] = None,
        user_data_causes_replacement: typing.Optional[builtins.bool] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        spot_options: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.LaunchTemplateSpotOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        spot_req_canceler_options: typing.Optional[typing.Union["SpotReqCancelerProps", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Properties of ``SpotInstance``.

        :param instance_type: Type of instance to launch.
        :param machine_image: AMI to launch.
        :param vpc: VPC to launch the instance in.
        :param allow_all_outbound: Whether the instance could initiate connections to anywhere by default. This property is only used when you do not provide a security group. Default: true
        :param availability_zone: In which AZ to place the instance within the VPC. Default: - Random zone.
        :param block_devices: Specifies how block devices are exposed to the instance. You can specify virtual devices and EBS volumes. Each instance that is launched has an associated root device volume, either an Amazon EBS volume or an instance store volume. You can use block device mappings to specify additional EBS volumes or instance store volumes to attach to an instance when it is launched. Default: - Uses the block device mapping of the AMI
        :param detailed_monitoring: Whether "Detailed Monitoring" is enabled for this instance Keep in mind that Detailed Monitoring results in extra charges. Default: - false
        :param init: Apply the given CloudFormation Init configuration to the instance at startup. Default: - no CloudFormation init
        :param init_options: Use the given options for applying CloudFormation Init. Describes the configsets to use and the timeout to wait Default: - default options
        :param instance_name: The name of the instance. Default: - CDK generated name
        :param key_name: Name of SSH keypair to grant access to instance. Default: - No SSH access will be possible.
        :param private_ip_address: Defines a private IP address to associate with an instance. Private IP should be available within the VPC that the instance is build within. Default: - no association
        :param propagate_tags_to_volume_on_creation: Propagate the EC2 instance tags to the EBS volumes. Default: - false
        :param require_imdsv2: Whether IMDSv2 should be required on this instance. Default: - false
        :param resource_signal_timeout: The length of time to wait for the resourceSignalCount. The maximum value is 43200 (12 hours). Default: Duration.minutes(5)
        :param role: An IAM role to associate with the instance profile assigned to this Auto Scaling Group. The role must be assumable by the service principal ``ec2.amazonaws.com``: Default: - A role will automatically be created, it can be accessed via the ``role`` property
        :param security_group: Security Group to assign to this instance. Default: - create new security group
        :param source_dest_check: Specifies whether to enable an instance launched in a VPC to perform NAT. This controls whether source/destination checking is enabled on the instance. A value of true means that checking is enabled, and false means that checking is disabled. The value must be false for the instance to perform NAT. Default: true
        :param user_data: Specific UserData to use. The UserData may still be mutated after creation. Default: - A UserData object appropriate for the MachineImage's Operating System is created.
        :param user_data_causes_replacement: Changes to the UserData force replacement. Depending the EC2 instance type, changing UserData either restarts the instance or replaces the instance. - Instance store-backed instances are replaced. - EBS-backed instances are restarted. By default, restarting does not execute the new UserData so you will need a different mechanism to ensure the instance is restarted. Setting this to ``true`` will make the instance's Logical ID depend on the UserData, which will cause CloudFormation to replace it if the UserData changes. Default: - true iff ``initOptions`` is specified, false otherwise.
        :param vpc_subnets: Where to place the instance within the VPC. Default: - Private subnets.
        :param spot_options: The options for the Spot instances. Default: - Use the Launch Template's default InstanceMarketOptions.
        :param spot_req_canceler_options: Options related to Lambda functions to cancel spot requests.
        '''
        if isinstance(init_options, dict):
            init_options = _aws_cdk_aws_ec2_ceddda9d.ApplyCloudFormationInitOptions(**init_options)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if isinstance(spot_options, dict):
            spot_options = _aws_cdk_aws_ec2_ceddda9d.LaunchTemplateSpotOptions(**spot_options)
        if isinstance(spot_req_canceler_options, dict):
            spot_req_canceler_options = SpotReqCancelerProps(**spot_req_canceler_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8816dad9fe7785001783bf19cc166c02eb0edb76c611ec7b8df2732098ac47fd)
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument machine_image", value=machine_image, expected_type=type_hints["machine_image"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument allow_all_outbound", value=allow_all_outbound, expected_type=type_hints["allow_all_outbound"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument block_devices", value=block_devices, expected_type=type_hints["block_devices"])
            check_type(argname="argument detailed_monitoring", value=detailed_monitoring, expected_type=type_hints["detailed_monitoring"])
            check_type(argname="argument init", value=init, expected_type=type_hints["init"])
            check_type(argname="argument init_options", value=init_options, expected_type=type_hints["init_options"])
            check_type(argname="argument instance_name", value=instance_name, expected_type=type_hints["instance_name"])
            check_type(argname="argument key_name", value=key_name, expected_type=type_hints["key_name"])
            check_type(argname="argument private_ip_address", value=private_ip_address, expected_type=type_hints["private_ip_address"])
            check_type(argname="argument propagate_tags_to_volume_on_creation", value=propagate_tags_to_volume_on_creation, expected_type=type_hints["propagate_tags_to_volume_on_creation"])
            check_type(argname="argument require_imdsv2", value=require_imdsv2, expected_type=type_hints["require_imdsv2"])
            check_type(argname="argument resource_signal_timeout", value=resource_signal_timeout, expected_type=type_hints["resource_signal_timeout"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument source_dest_check", value=source_dest_check, expected_type=type_hints["source_dest_check"])
            check_type(argname="argument user_data", value=user_data, expected_type=type_hints["user_data"])
            check_type(argname="argument user_data_causes_replacement", value=user_data_causes_replacement, expected_type=type_hints["user_data_causes_replacement"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
            check_type(argname="argument spot_options", value=spot_options, expected_type=type_hints["spot_options"])
            check_type(argname="argument spot_req_canceler_options", value=spot_req_canceler_options, expected_type=type_hints["spot_req_canceler_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_type": instance_type,
            "machine_image": machine_image,
            "vpc": vpc,
        }
        if allow_all_outbound is not None:
            self._values["allow_all_outbound"] = allow_all_outbound
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if block_devices is not None:
            self._values["block_devices"] = block_devices
        if detailed_monitoring is not None:
            self._values["detailed_monitoring"] = detailed_monitoring
        if init is not None:
            self._values["init"] = init
        if init_options is not None:
            self._values["init_options"] = init_options
        if instance_name is not None:
            self._values["instance_name"] = instance_name
        if key_name is not None:
            self._values["key_name"] = key_name
        if private_ip_address is not None:
            self._values["private_ip_address"] = private_ip_address
        if propagate_tags_to_volume_on_creation is not None:
            self._values["propagate_tags_to_volume_on_creation"] = propagate_tags_to_volume_on_creation
        if require_imdsv2 is not None:
            self._values["require_imdsv2"] = require_imdsv2
        if resource_signal_timeout is not None:
            self._values["resource_signal_timeout"] = resource_signal_timeout
        if role is not None:
            self._values["role"] = role
        if security_group is not None:
            self._values["security_group"] = security_group
        if source_dest_check is not None:
            self._values["source_dest_check"] = source_dest_check
        if user_data is not None:
            self._values["user_data"] = user_data
        if user_data_causes_replacement is not None:
            self._values["user_data_causes_replacement"] = user_data_causes_replacement
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if spot_options is not None:
            self._values["spot_options"] = spot_options
        if spot_req_canceler_options is not None:
            self._values["spot_req_canceler_options"] = spot_req_canceler_options

    @builtins.property
    def instance_type(self) -> _aws_cdk_aws_ec2_ceddda9d.InstanceType:
        '''Type of instance to launch.'''
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.InstanceType, result)

    @builtins.property
    def machine_image(self) -> _aws_cdk_aws_ec2_ceddda9d.IMachineImage:
        '''AMI to launch.'''
        result = self._values.get("machine_image")
        assert result is not None, "Required property 'machine_image' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IMachineImage, result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''VPC to launch the instance in.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def allow_all_outbound(self) -> typing.Optional[builtins.bool]:
        '''Whether the instance could initiate connections to anywhere by default.

        This property is only used when you do not provide a security group.

        :default: true
        '''
        result = self._values.get("allow_all_outbound")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''In which AZ to place the instance within the VPC.

        :default: - Random zone.
        '''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def block_devices(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.BlockDevice]]:
        '''Specifies how block devices are exposed to the instance. You can specify virtual devices and EBS volumes.

        Each instance that is launched has an associated root device volume,
        either an Amazon EBS volume or an instance store volume.
        You can use block device mappings to specify additional EBS volumes or
        instance store volumes to attach to an instance when it is launched.

        :default: - Uses the block device mapping of the AMI

        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/block-device-mapping-concepts.html
        '''
        result = self._values.get("block_devices")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.BlockDevice]], result)

    @builtins.property
    def detailed_monitoring(self) -> typing.Optional[builtins.bool]:
        '''Whether "Detailed Monitoring" is enabled for this instance Keep in mind that Detailed Monitoring results in extra charges.

        :default: - false

        :see: http://aws.amazon.com/cloudwatch/pricing/
        '''
        result = self._values.get("detailed_monitoring")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def init(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.CloudFormationInit]:
        '''Apply the given CloudFormation Init configuration to the instance at startup.

        :default: - no CloudFormation init
        '''
        result = self._values.get("init")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.CloudFormationInit], result)

    @builtins.property
    def init_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ApplyCloudFormationInitOptions]:
        '''Use the given options for applying CloudFormation Init.

        Describes the configsets to use and the timeout to wait

        :default: - default options
        '''
        result = self._values.get("init_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ApplyCloudFormationInitOptions], result)

    @builtins.property
    def instance_name(self) -> typing.Optional[builtins.str]:
        '''The name of the instance.

        :default: - CDK generated name
        '''
        result = self._values.get("instance_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_name(self) -> typing.Optional[builtins.str]:
        '''Name of SSH keypair to grant access to instance.

        :default: - No SSH access will be possible.
        '''
        result = self._values.get("key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_ip_address(self) -> typing.Optional[builtins.str]:
        '''Defines a private IP address to associate with an instance.

        Private IP should be available within the VPC that the instance is build within.

        :default: - no association
        '''
        result = self._values.get("private_ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def propagate_tags_to_volume_on_creation(self) -> typing.Optional[builtins.bool]:
        '''Propagate the EC2 instance tags to the EBS volumes.

        :default: - false
        '''
        result = self._values.get("propagate_tags_to_volume_on_creation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def require_imdsv2(self) -> typing.Optional[builtins.bool]:
        '''Whether IMDSv2 should be required on this instance.

        :default: - false
        '''
        result = self._values.get("require_imdsv2")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def resource_signal_timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The length of time to wait for the resourceSignalCount.

        The maximum value is 43200 (12 hours).

        :default: Duration.minutes(5)
        '''
        result = self._values.get("resource_signal_timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''An IAM role to associate with the instance profile assigned to this Auto Scaling Group.

        The role must be assumable by the service principal ``ec2.amazonaws.com``:

        :default: - A role will automatically be created, it can be accessed via the ``role`` property

        Example::

            const role = new iam.Role(this, 'MyRole', {
              assumedBy: new iam.ServicePrincipal('ec2.amazonaws.com')
            });
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''Security Group to assign to this instance.

        :default: - create new security group
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], result)

    @builtins.property
    def source_dest_check(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether to enable an instance launched in a VPC to perform NAT.

        This controls whether source/destination checking is enabled on the instance.
        A value of true means that checking is enabled, and false means that checking is disabled.
        The value must be false for the instance to perform NAT.

        :default: true
        '''
        result = self._values.get("source_dest_check")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def user_data(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData]:
        '''Specific UserData to use.

        The UserData may still be mutated after creation.

        :default:

        - A UserData object appropriate for the MachineImage's
        Operating System is created.
        '''
        result = self._values.get("user_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData], result)

    @builtins.property
    def user_data_causes_replacement(self) -> typing.Optional[builtins.bool]:
        '''Changes to the UserData force replacement.

        Depending the EC2 instance type, changing UserData either
        restarts the instance or replaces the instance.

        - Instance store-backed instances are replaced.
        - EBS-backed instances are restarted.

        By default, restarting does not execute the new UserData so you
        will need a different mechanism to ensure the instance is restarted.

        Setting this to ``true`` will make the instance's Logical ID depend on the
        UserData, which will cause CloudFormation to replace it if the UserData
        changes.

        :default: - true iff ``initOptions`` is specified, false otherwise.
        '''
        result = self._values.get("user_data_causes_replacement")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''Where to place the instance within the VPC.

        :default: - Private subnets.
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def spot_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.LaunchTemplateSpotOptions]:
        '''The options for the Spot instances.

        :default: - Use the Launch Template's default InstanceMarketOptions.
        '''
        result = self._values.get("spot_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.LaunchTemplateSpotOptions], result)

    @builtins.property
    def spot_req_canceler_options(self) -> typing.Optional["SpotReqCancelerProps"]:
        '''Options related to Lambda functions to cancel spot requests.'''
        result = self._values.get("spot_req_canceler_options")
        return typing.cast(typing.Optional["SpotReqCancelerProps"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpotInstanceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-ec2-spot-simple.SpotReqCancelerProps",
    jsii_struct_bases=[],
    name_mapping={
        "lambda_excecution_role": "lambdaExcecutionRole",
        "lambda_log_retention": "lambdaLogRetention",
        "lambda_runtime": "lambdaRuntime",
    },
)
class SpotReqCancelerProps:
    def __init__(
        self,
        *,
        lambda_excecution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        lambda_log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        lambda_runtime: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Runtime] = None,
    ) -> None:
        '''Options related to Lambda functions to cancel spot requests.

        :param lambda_excecution_role: Internal Lambda functions execution role. Default: - Create a new Role that can do ec2:DescribeInstances and ec2:CancelSpotInstanceRequests and has "service-role/AWSLambdaBasicExecutionRole"
        :param lambda_log_retention: Log retention period for internal Lambda functions logs kept in CloudWatch Logs. Default: - Three months
        :param lambda_runtime: Runtime environment for the internal Lambda function. If anything other than Node.js is specified, an error will occur. Default: - Node.js 16
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11798b5c3f8cf57d4edb29a5bf3c4d336f7b5b826f3f2fab749716e4d74f6370)
            check_type(argname="argument lambda_excecution_role", value=lambda_excecution_role, expected_type=type_hints["lambda_excecution_role"])
            check_type(argname="argument lambda_log_retention", value=lambda_log_retention, expected_type=type_hints["lambda_log_retention"])
            check_type(argname="argument lambda_runtime", value=lambda_runtime, expected_type=type_hints["lambda_runtime"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if lambda_excecution_role is not None:
            self._values["lambda_excecution_role"] = lambda_excecution_role
        if lambda_log_retention is not None:
            self._values["lambda_log_retention"] = lambda_log_retention
        if lambda_runtime is not None:
            self._values["lambda_runtime"] = lambda_runtime

    @builtins.property
    def lambda_excecution_role(
        self,
    ) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''Internal Lambda functions execution role.

        :default: - Create a new Role that can do ec2:DescribeInstances and ec2:CancelSpotInstanceRequests and has "service-role/AWSLambdaBasicExecutionRole"
        '''
        result = self._values.get("lambda_excecution_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def lambda_log_retention(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays]:
        '''Log retention period for internal Lambda functions logs kept in CloudWatch Logs.

        :default: - Three months
        '''
        result = self._values.get("lambda_log_retention")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays], result)

    @builtins.property
    def lambda_runtime(self) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Runtime]:
        '''Runtime environment for the internal Lambda function.

        If anything other than Node.js is specified, an error will occur.

        :default: - Node.js 16
        '''
        result = self._values.get("lambda_runtime")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Runtime], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpotReqCancelerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "SpotInstance",
    "SpotInstanceProps",
    "SpotReqCancelerProps",
]

publication.publish()

def _typecheckingstub__051e0cc92650cdd834123f9ea5d7c961a30feed47306a6a346d2f06e3774662b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    spot_options: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.LaunchTemplateSpotOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    spot_req_canceler_options: typing.Optional[typing.Union[SpotReqCancelerProps, typing.Dict[builtins.str, typing.Any]]] = None,
    instance_type: _aws_cdk_aws_ec2_ceddda9d.InstanceType,
    machine_image: _aws_cdk_aws_ec2_ceddda9d.IMachineImage,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    allow_all_outbound: typing.Optional[builtins.bool] = None,
    availability_zone: typing.Optional[builtins.str] = None,
    block_devices: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.BlockDevice, typing.Dict[builtins.str, typing.Any]]]] = None,
    detailed_monitoring: typing.Optional[builtins.bool] = None,
    init: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.CloudFormationInit] = None,
    init_options: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.ApplyCloudFormationInitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    instance_name: typing.Optional[builtins.str] = None,
    key_name: typing.Optional[builtins.str] = None,
    private_ip_address: typing.Optional[builtins.str] = None,
    propagate_tags_to_volume_on_creation: typing.Optional[builtins.bool] = None,
    require_imdsv2: typing.Optional[builtins.bool] = None,
    resource_signal_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    source_dest_check: typing.Optional[builtins.bool] = None,
    user_data: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData] = None,
    user_data_causes_replacement: typing.Optional[builtins.bool] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8816dad9fe7785001783bf19cc166c02eb0edb76c611ec7b8df2732098ac47fd(
    *,
    instance_type: _aws_cdk_aws_ec2_ceddda9d.InstanceType,
    machine_image: _aws_cdk_aws_ec2_ceddda9d.IMachineImage,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    allow_all_outbound: typing.Optional[builtins.bool] = None,
    availability_zone: typing.Optional[builtins.str] = None,
    block_devices: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.BlockDevice, typing.Dict[builtins.str, typing.Any]]]] = None,
    detailed_monitoring: typing.Optional[builtins.bool] = None,
    init: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.CloudFormationInit] = None,
    init_options: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.ApplyCloudFormationInitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    instance_name: typing.Optional[builtins.str] = None,
    key_name: typing.Optional[builtins.str] = None,
    private_ip_address: typing.Optional[builtins.str] = None,
    propagate_tags_to_volume_on_creation: typing.Optional[builtins.bool] = None,
    require_imdsv2: typing.Optional[builtins.bool] = None,
    resource_signal_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    source_dest_check: typing.Optional[builtins.bool] = None,
    user_data: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData] = None,
    user_data_causes_replacement: typing.Optional[builtins.bool] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    spot_options: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.LaunchTemplateSpotOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    spot_req_canceler_options: typing.Optional[typing.Union[SpotReqCancelerProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11798b5c3f8cf57d4edb29a5bf3c4d336f7b5b826f3f2fab749716e4d74f6370(
    *,
    lambda_excecution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    lambda_log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    lambda_runtime: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Runtime] = None,
) -> None:
    """Type checking stubs"""
    pass
