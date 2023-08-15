'''
[![NPM version](https://badge.fury.io/js/cdk-keycloak.svg)](https://badge.fury.io/js/cdk-keycloak)
[![PyPI version](https://badge.fury.io/py/cdk-keycloak.svg)](https://badge.fury.io/py/cdk-keycloak)
[![release](https://github.com/aws-samples/cdk-keycloak/actions/workflows/release.yml/badge.svg)](https://github.com/aws-samples/cdk-keycloak/actions/workflows/release.yml)

# `cdk-keycloak`

CDK construct library that allows you to create [KeyCloak](https://www.keycloak.org/) on AWS in TypeScript or Python

> **Note**
>
> This project has been migrated to CDK v2.
>
> CDK v1 compatible version is deprecated now.

# Sample

```python
import { KeyCloak } from 'cdk-keycloak';

const app = new cdk.App();

const env = {
  region: process.env.CDK_DEFAULT_REGION,
  account: process.env.CDK_DEFAULT_ACCOUNT,
};

const stack = new cdk.Stack(app, 'keycloak-demo', { env });
new KeyCloak(stack, 'KeyCloak', {
  certificateArn: 'arn:aws:acm:us-east-1:123456789012:certificate/293cf875-ca98-4c2e-a797-e1cf6df2553c',
  keycloakVersion,
});
```

# Keycloak version pinning

Use `keycloakVersion` to specify the version.

```python
new KeyCloak(stack, 'KeyCloak', {
  certificateArn,
  keycloakVersion: KeycloakVersion.V15_0_2,
});
```

To specify any other verion not defined in the construct, use `KeycloakVersion.of('x.x.x')`. This allows you to specify any new version as soon as it's available. However, as new versions will not always be tested and validated with this construct library, make sure you fully backup and test before you use any new version in the production environment.

# Aurora Serverless support

The `KeyCloak` construct provisions the **Amaozn RDS cluster for MySQL** with **2** database instances under the hood, to opt in **Amazon Aurora Serverless**, use `auroraServerless` to opt in Amazon Aurora Serverless cluster. Please note only some regions are supported, check [Supported features in Amazon Aurora by AWS Region and Aurora DB engine](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Concepts.AuroraFeaturesRegionsDBEngines.grids.html) for availability.

```python
// Aurora Serverless v1
new KeyCloak(stack, 'KeyCloak', {
  certificateArn,
  auroraServerless: true,
  keycloakVersion,
});

// Aurora Serverless v2
new KeyCloak(stack, 'KeyCloak', {
  certificateArn,
  auroraServerlessV2: true,
  keycloakVersion,
});
```

Behind the scene, a default RDS cluster for MySQL with 2 database instances will be created.

# Opt-in for Single RDS instance

To create single RDS instance for your testing or development environment, use `singleDbInstance` to turn on the
single db instance deployment.

Plesae note this is not recommended for production environment.

```python
new KeyCloak(stack, 'KeyCloak', {
  certificateArn,
  singleDbInstance: true,
  keycloakVersion,
});
```

# Service Auto Scaling

Define `autoScaleTask` for the ecs service task autoscaling. For example:

```python
new KeyCloak(stack, 'KeyCloak', {
  auroraServerless: true,
  nodeCount: 2,
  autoScaleTask: {
    min: 2,
    max: 10,
    targetCpuUtilization: 60,
  },
});
```

# Customize fargate task settings

Define `taskCpu` or `taskMemory` for overriding the defaults for the ecs service task.
Could be useful for development environments. For example:

```python
new KeyCloak(stack, 'KeyCloak', {
  nodeCount: 1,
  taskCpu: 512,
  taskMemory: 2048,
});
```

# Deploy in existing Vpc Subnets

You can deploy the workload in the existing Vpc and subnets. The `publicSubnets` are for the ALB, `privateSubnets` for the keycloak container tasks and `databaseSubnets` for the database.

The best practice is to specify isolated subnets for `databaseSubnets`, however, in some cases might have no existing isolates subnets then the private subnets are also acceptable.

Consider the sample below:

```python
new KeyCloak(stack, 'KeyCloak', {
  certificateArn: 'arn:aws:acm:us-east-1:123456789012:certificate/293cf875-ca98-4c2e-a797-e1cf6df2553c',
  vpc: ec2.Vpc.fromLookup(stack, 'Vpc', { vpcId: 'vpc-0417e46d' }),
  publicSubnets: {
    subnets: [
      ec2.Subnet.fromSubnetId(stack, 'pub-1a', 'subnet-5bbe7b32'),
      ec2.Subnet.fromSubnetId(stack, 'pub-1b', 'subnet-0428367c'),
      ec2.Subnet.fromSubnetId(stack, 'pub-1c', 'subnet-1586a75f'),
    ],
  },
  privateSubnets: {
    subnets: [
      ec2.Subnet.fromSubnetId(stack, 'priv-1a', 'subnet-0e9460dbcfc4cf6ee'),
      ec2.Subnet.fromSubnetId(stack, 'priv-1b', 'subnet-0562f666bdf5c29af'),
      ec2.Subnet.fromSubnetId(stack, 'priv-1c', 'subnet-00ab15c0022872f06'),
    ],
  },
  databaseSubnets: {
    subnets: [
      ec2.Subnet.fromSubnetId(stack, 'db-1a', 'subnet-0e9460dbcfc4cf6ee'),
      ec2.Subnet.fromSubnetId(stack, 'db-1b', 'subnet-0562f666bdf5c29af'),
      ec2.Subnet.fromSubnetId(stack, 'db-1c', 'subnet-00ab15c0022872f06'),
    ],
  },
});
```

# AWS China Regions

This library support AWS China regions `cn-north-1` and `cn-northwest-1` and will auto select local docker image mirror to accelerate the image pulling. You don't have to do anything.

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This project is licensed under the Apache-2.0 License.
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
import aws_cdk.aws_certificatemanager as _aws_cdk_aws_certificatemanager_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_ecs as _aws_cdk_aws_ecs_ceddda9d
import aws_cdk.aws_elasticloadbalancingv2 as _aws_cdk_aws_elasticloadbalancingv2_ceddda9d
import aws_cdk.aws_rds as _aws_cdk_aws_rds_ceddda9d
import aws_cdk.aws_secretsmanager as _aws_cdk_aws_secretsmanager_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="cdk-keycloak.AutoScaleTask",
    jsii_struct_bases=[],
    name_mapping={
        "max": "max",
        "min": "min",
        "target_cpu_utilization": "targetCpuUtilization",
    },
)
class AutoScaleTask:
    def __init__(
        self,
        *,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
        target_cpu_utilization: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''The ECS task autoscaling definition.

        :param max: The maximal count of the task number. Default: - min + 5
        :param min: The minimal count of the task number. Default: - nodeCount
        :param target_cpu_utilization: The target cpu utilization for the service autoscaling. Default: 75
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3b0ccd8e2d54fa02d4baf3cc34671d011fbd811398e0fa7705a0176c146a0d4)
            check_type(argname="argument max", value=max, expected_type=type_hints["max"])
            check_type(argname="argument min", value=min, expected_type=type_hints["min"])
            check_type(argname="argument target_cpu_utilization", value=target_cpu_utilization, expected_type=type_hints["target_cpu_utilization"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max is not None:
            self._values["max"] = max
        if min is not None:
            self._values["min"] = min
        if target_cpu_utilization is not None:
            self._values["target_cpu_utilization"] = target_cpu_utilization

    @builtins.property
    def max(self) -> typing.Optional[jsii.Number]:
        '''The maximal count of the task number.

        :default: - min + 5
        '''
        result = self._values.get("max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min(self) -> typing.Optional[jsii.Number]:
        '''The minimal count of the task number.

        :default: - nodeCount
        '''
        result = self._values.get("min")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_cpu_utilization(self) -> typing.Optional[jsii.Number]:
        '''The target cpu utilization for the service autoscaling.

        :default: 75
        '''
        result = self._values.get("target_cpu_utilization")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutoScaleTask(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerService(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-keycloak.ContainerService",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        certificate: _aws_cdk_aws_certificatemanager_ceddda9d.ICertificate,
        database: "Database",
        keycloak_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        keycloak_version: "KeycloakVersion",
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        auto_scale_task: typing.Optional[typing.Union[AutoScaleTask, typing.Dict[builtins.str, typing.Any]]] = None,
        bastion: typing.Optional[builtins.bool] = None,
        circuit_breaker: typing.Optional[builtins.bool] = None,
        container_image: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ContainerImage] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        hostname: typing.Optional[builtins.str] = None,
        internet_facing: typing.Optional[builtins.bool] = None,
        node_count: typing.Optional[jsii.Number] = None,
        private_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        public_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        stickiness_cookie_duration: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        task_cpu: typing.Optional[jsii.Number] = None,
        task_memory: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param certificate: The ACM certificate.
        :param database: The RDS database for the service.
        :param keycloak_secret: The secrets manager secret for the keycloak.
        :param keycloak_version: Keycloak version for the container image.
        :param vpc: The VPC for the service.
        :param auto_scale_task: Autoscaling for the ECS Service. Default: - no ecs service autoscaling
        :param bastion: Whether to create the bastion host. Default: false
        :param circuit_breaker: Whether to enable the ECS service deployment circuit breaker. Default: false
        :param container_image: Overrides the default image. Default: quay.io/keycloak/keycloak:${KEYCLOAK_VERSION}
        :param env: The environment variables to pass to the keycloak container.
        :param hostname: The hostname to use for the keycloak server.
        :param internet_facing: Whether to put the put the load balancer in the public or private subnets. Default: true
        :param node_count: Number of keycloak node in the cluster. Default: 1
        :param private_subnets: VPC subnets for keycloak service.
        :param public_subnets: VPC public subnets for ALB.
        :param stickiness_cookie_duration: The sticky session duration for the keycloak workload with ALB. Default: - one day
        :param task_cpu: The number of cpu units used by the keycloak task. Default: 4096
        :param task_memory: The amount (in MiB) of memory used by the keycloak task. Default: 8192
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0c2eef21e65e800e7034a8c9b53d89aa03dfe5a2dd0aa1ed8c3e20958b2e22d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ContainerServiceProps(
            certificate=certificate,
            database=database,
            keycloak_secret=keycloak_secret,
            keycloak_version=keycloak_version,
            vpc=vpc,
            auto_scale_task=auto_scale_task,
            bastion=bastion,
            circuit_breaker=circuit_breaker,
            container_image=container_image,
            env=env,
            hostname=hostname,
            internet_facing=internet_facing,
            node_count=node_count,
            private_subnets=private_subnets,
            public_subnets=public_subnets,
            stickiness_cookie_duration=stickiness_cookie_duration,
            task_cpu=task_cpu,
            task_memory=task_memory,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="applicationLoadBalancer")
    def application_load_balancer(
        self,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationLoadBalancer:
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationLoadBalancer, jsii.get(self, "applicationLoadBalancer"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> _aws_cdk_aws_ecs_ceddda9d.FargateService:
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.FargateService, jsii.get(self, "service"))


@jsii.data_type(
    jsii_type="cdk-keycloak.ContainerServiceProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate": "certificate",
        "database": "database",
        "keycloak_secret": "keycloakSecret",
        "keycloak_version": "keycloakVersion",
        "vpc": "vpc",
        "auto_scale_task": "autoScaleTask",
        "bastion": "bastion",
        "circuit_breaker": "circuitBreaker",
        "container_image": "containerImage",
        "env": "env",
        "hostname": "hostname",
        "internet_facing": "internetFacing",
        "node_count": "nodeCount",
        "private_subnets": "privateSubnets",
        "public_subnets": "publicSubnets",
        "stickiness_cookie_duration": "stickinessCookieDuration",
        "task_cpu": "taskCpu",
        "task_memory": "taskMemory",
    },
)
class ContainerServiceProps:
    def __init__(
        self,
        *,
        certificate: _aws_cdk_aws_certificatemanager_ceddda9d.ICertificate,
        database: "Database",
        keycloak_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        keycloak_version: "KeycloakVersion",
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        auto_scale_task: typing.Optional[typing.Union[AutoScaleTask, typing.Dict[builtins.str, typing.Any]]] = None,
        bastion: typing.Optional[builtins.bool] = None,
        circuit_breaker: typing.Optional[builtins.bool] = None,
        container_image: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ContainerImage] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        hostname: typing.Optional[builtins.str] = None,
        internet_facing: typing.Optional[builtins.bool] = None,
        node_count: typing.Optional[jsii.Number] = None,
        private_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        public_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        stickiness_cookie_duration: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        task_cpu: typing.Optional[jsii.Number] = None,
        task_memory: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param certificate: The ACM certificate.
        :param database: The RDS database for the service.
        :param keycloak_secret: The secrets manager secret for the keycloak.
        :param keycloak_version: Keycloak version for the container image.
        :param vpc: The VPC for the service.
        :param auto_scale_task: Autoscaling for the ECS Service. Default: - no ecs service autoscaling
        :param bastion: Whether to create the bastion host. Default: false
        :param circuit_breaker: Whether to enable the ECS service deployment circuit breaker. Default: false
        :param container_image: Overrides the default image. Default: quay.io/keycloak/keycloak:${KEYCLOAK_VERSION}
        :param env: The environment variables to pass to the keycloak container.
        :param hostname: The hostname to use for the keycloak server.
        :param internet_facing: Whether to put the put the load balancer in the public or private subnets. Default: true
        :param node_count: Number of keycloak node in the cluster. Default: 1
        :param private_subnets: VPC subnets for keycloak service.
        :param public_subnets: VPC public subnets for ALB.
        :param stickiness_cookie_duration: The sticky session duration for the keycloak workload with ALB. Default: - one day
        :param task_cpu: The number of cpu units used by the keycloak task. Default: 4096
        :param task_memory: The amount (in MiB) of memory used by the keycloak task. Default: 8192
        '''
        if isinstance(auto_scale_task, dict):
            auto_scale_task = AutoScaleTask(**auto_scale_task)
        if isinstance(private_subnets, dict):
            private_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**private_subnets)
        if isinstance(public_subnets, dict):
            public_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**public_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9423892d53ff57f474e07d6df4106ed0c077ac7a49f4d418a8e9c71ae627396e)
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument keycloak_secret", value=keycloak_secret, expected_type=type_hints["keycloak_secret"])
            check_type(argname="argument keycloak_version", value=keycloak_version, expected_type=type_hints["keycloak_version"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument auto_scale_task", value=auto_scale_task, expected_type=type_hints["auto_scale_task"])
            check_type(argname="argument bastion", value=bastion, expected_type=type_hints["bastion"])
            check_type(argname="argument circuit_breaker", value=circuit_breaker, expected_type=type_hints["circuit_breaker"])
            check_type(argname="argument container_image", value=container_image, expected_type=type_hints["container_image"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument internet_facing", value=internet_facing, expected_type=type_hints["internet_facing"])
            check_type(argname="argument node_count", value=node_count, expected_type=type_hints["node_count"])
            check_type(argname="argument private_subnets", value=private_subnets, expected_type=type_hints["private_subnets"])
            check_type(argname="argument public_subnets", value=public_subnets, expected_type=type_hints["public_subnets"])
            check_type(argname="argument stickiness_cookie_duration", value=stickiness_cookie_duration, expected_type=type_hints["stickiness_cookie_duration"])
            check_type(argname="argument task_cpu", value=task_cpu, expected_type=type_hints["task_cpu"])
            check_type(argname="argument task_memory", value=task_memory, expected_type=type_hints["task_memory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "certificate": certificate,
            "database": database,
            "keycloak_secret": keycloak_secret,
            "keycloak_version": keycloak_version,
            "vpc": vpc,
        }
        if auto_scale_task is not None:
            self._values["auto_scale_task"] = auto_scale_task
        if bastion is not None:
            self._values["bastion"] = bastion
        if circuit_breaker is not None:
            self._values["circuit_breaker"] = circuit_breaker
        if container_image is not None:
            self._values["container_image"] = container_image
        if env is not None:
            self._values["env"] = env
        if hostname is not None:
            self._values["hostname"] = hostname
        if internet_facing is not None:
            self._values["internet_facing"] = internet_facing
        if node_count is not None:
            self._values["node_count"] = node_count
        if private_subnets is not None:
            self._values["private_subnets"] = private_subnets
        if public_subnets is not None:
            self._values["public_subnets"] = public_subnets
        if stickiness_cookie_duration is not None:
            self._values["stickiness_cookie_duration"] = stickiness_cookie_duration
        if task_cpu is not None:
            self._values["task_cpu"] = task_cpu
        if task_memory is not None:
            self._values["task_memory"] = task_memory

    @builtins.property
    def certificate(self) -> _aws_cdk_aws_certificatemanager_ceddda9d.ICertificate:
        '''The ACM certificate.'''
        result = self._values.get("certificate")
        assert result is not None, "Required property 'certificate' is missing"
        return typing.cast(_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate, result)

    @builtins.property
    def database(self) -> "Database":
        '''The RDS database for the service.'''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast("Database", result)

    @builtins.property
    def keycloak_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''The secrets manager secret for the keycloak.'''
        result = self._values.get("keycloak_secret")
        assert result is not None, "Required property 'keycloak_secret' is missing"
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, result)

    @builtins.property
    def keycloak_version(self) -> "KeycloakVersion":
        '''Keycloak version for the container image.'''
        result = self._values.get("keycloak_version")
        assert result is not None, "Required property 'keycloak_version' is missing"
        return typing.cast("KeycloakVersion", result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The VPC for the service.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def auto_scale_task(self) -> typing.Optional[AutoScaleTask]:
        '''Autoscaling for the ECS Service.

        :default: - no ecs service autoscaling
        '''
        result = self._values.get("auto_scale_task")
        return typing.cast(typing.Optional[AutoScaleTask], result)

    @builtins.property
    def bastion(self) -> typing.Optional[builtins.bool]:
        '''Whether to create the bastion host.

        :default: false
        '''
        result = self._values.get("bastion")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def circuit_breaker(self) -> typing.Optional[builtins.bool]:
        '''Whether to enable the ECS service deployment circuit breaker.

        :default: false
        '''
        result = self._values.get("circuit_breaker")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def container_image(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ContainerImage]:
        '''Overrides the default image.

        :default: quay.io/keycloak/keycloak:${KEYCLOAK_VERSION}
        '''
        result = self._values.get("container_image")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ContainerImage], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The environment variables to pass to the keycloak container.'''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def hostname(self) -> typing.Optional[builtins.str]:
        '''The hostname to use for the keycloak server.'''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def internet_facing(self) -> typing.Optional[builtins.bool]:
        '''Whether to put the put the load balancer in the public or private subnets.

        :default: true
        '''
        result = self._values.get("internet_facing")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def node_count(self) -> typing.Optional[jsii.Number]:
        '''Number of keycloak node in the cluster.

        :default: 1
        '''
        result = self._values.get("node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def private_subnets(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''VPC subnets for keycloak service.'''
        result = self._values.get("private_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def public_subnets(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''VPC public subnets for ALB.'''
        result = self._values.get("public_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def stickiness_cookie_duration(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The sticky session duration for the keycloak workload with ALB.

        :default: - one day
        '''
        result = self._values.get("stickiness_cookie_duration")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def task_cpu(self) -> typing.Optional[jsii.Number]:
        '''The number of cpu units used by the keycloak task.

        :default: 4096

        :see: FargateTaskDefinitionProps
        '''
        result = self._values.get("task_cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def task_memory(self) -> typing.Optional[jsii.Number]:
        '''The amount (in MiB) of memory used by the keycloak task.

        :default: 8192

        :see: FargateTaskDefinitionProps
        '''
        result = self._values.get("task_memory")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Database(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-keycloak.Database",
):
    '''Represents the database instance or database cluster.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        aurora_serverless: typing.Optional[builtins.bool] = None,
        aurora_serverless_v2: typing.Optional[builtins.bool] = None,
        backup_retention: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        cluster_engine: typing.Optional[_aws_cdk_aws_rds_ceddda9d.IClusterEngine] = None,
        database_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        instance_engine: typing.Optional[_aws_cdk_aws_rds_ceddda9d.IInstanceEngine] = None,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        single_db_instance: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param vpc: The VPC for the database.
        :param aurora_serverless: enable aurora serverless. Default: false
        :param aurora_serverless_v2: enable aurora serverless v2. Default: false
        :param backup_retention: database backup retension. Default: - 7 days
        :param cluster_engine: The database cluster engine. Default: rds.AuroraMysqlEngineVersion.VER_2_09_1
        :param database_subnets: VPC subnets for database.
        :param instance_engine: The database instance engine. Default: - MySQL 8.0.21
        :param instance_type: The database instance type. Default: r5.large
        :param max_capacity: The maximum number of Aurora Serverless V2 capacity units. Default: 10
        :param min_capacity: The minimum number of Aurora Serverless V2 capacity units. Default: 0.5
        :param removal_policy: Controls what happens to the database if it stops being managed by CloudFormation. Default: RemovalPolicy.RETAIN
        :param single_db_instance: Whether to use single RDS instance rather than RDS cluster. Not recommended for production. Default: false
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__669d3357a4af4b4c29dded87b17f644277319118760adce20d6b09577165a6be)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DatabaseProps(
            vpc=vpc,
            aurora_serverless=aurora_serverless,
            aurora_serverless_v2=aurora_serverless_v2,
            backup_retention=backup_retention,
            cluster_engine=cluster_engine,
            database_subnets=database_subnets,
            instance_engine=instance_engine,
            instance_type=instance_type,
            max_capacity=max_capacity,
            min_capacity=min_capacity,
            removal_policy=removal_policy,
            single_db_instance=single_db_instance,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="clusterEndpointHostname")
    def cluster_endpoint_hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterEndpointHostname"))

    @builtins.property
    @jsii.member(jsii_name="clusterIdentifier")
    def cluster_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterIdentifier"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _aws_cdk_aws_ec2_ceddda9d.Connections:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Connections, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, jsii.get(self, "secret"))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, jsii.get(self, "vpc"))


@jsii.data_type(
    jsii_type="cdk-keycloak.DatabaseConfig",
    jsii_struct_bases=[],
    name_mapping={
        "connections": "connections",
        "endpoint": "endpoint",
        "identifier": "identifier",
        "secret": "secret",
    },
)
class DatabaseConfig:
    def __init__(
        self,
        *,
        connections: _aws_cdk_aws_ec2_ceddda9d.Connections,
        endpoint: builtins.str,
        identifier: builtins.str,
        secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    ) -> None:
        '''Database configuration.

        :param connections: The database connnections.
        :param endpoint: The endpoint address for the database.
        :param identifier: The databasae identifier.
        :param secret: The database secret.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dd52df53ef0f251d7b54810cc7cf33131743e97e18104fa376c9ff477e9be0a)
            check_type(argname="argument connections", value=connections, expected_type=type_hints["connections"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument identifier", value=identifier, expected_type=type_hints["identifier"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "connections": connections,
            "endpoint": endpoint,
            "identifier": identifier,
            "secret": secret,
        }

    @builtins.property
    def connections(self) -> _aws_cdk_aws_ec2_ceddda9d.Connections:
        '''The database connnections.'''
        result = self._values.get("connections")
        assert result is not None, "Required property 'connections' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Connections, result)

    @builtins.property
    def endpoint(self) -> builtins.str:
        '''The endpoint address for the database.'''
        result = self._values.get("endpoint")
        assert result is not None, "Required property 'endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identifier(self) -> builtins.str:
        '''The databasae identifier.'''
        result = self._values.get("identifier")
        assert result is not None, "Required property 'identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''The database secret.'''
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-keycloak.DatabaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "vpc": "vpc",
        "aurora_serverless": "auroraServerless",
        "aurora_serverless_v2": "auroraServerlessV2",
        "backup_retention": "backupRetention",
        "cluster_engine": "clusterEngine",
        "database_subnets": "databaseSubnets",
        "instance_engine": "instanceEngine",
        "instance_type": "instanceType",
        "max_capacity": "maxCapacity",
        "min_capacity": "minCapacity",
        "removal_policy": "removalPolicy",
        "single_db_instance": "singleDbInstance",
    },
)
class DatabaseProps:
    def __init__(
        self,
        *,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        aurora_serverless: typing.Optional[builtins.bool] = None,
        aurora_serverless_v2: typing.Optional[builtins.bool] = None,
        backup_retention: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        cluster_engine: typing.Optional[_aws_cdk_aws_rds_ceddda9d.IClusterEngine] = None,
        database_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        instance_engine: typing.Optional[_aws_cdk_aws_rds_ceddda9d.IInstanceEngine] = None,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        single_db_instance: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param vpc: The VPC for the database.
        :param aurora_serverless: enable aurora serverless. Default: false
        :param aurora_serverless_v2: enable aurora serverless v2. Default: false
        :param backup_retention: database backup retension. Default: - 7 days
        :param cluster_engine: The database cluster engine. Default: rds.AuroraMysqlEngineVersion.VER_2_09_1
        :param database_subnets: VPC subnets for database.
        :param instance_engine: The database instance engine. Default: - MySQL 8.0.21
        :param instance_type: The database instance type. Default: r5.large
        :param max_capacity: The maximum number of Aurora Serverless V2 capacity units. Default: 10
        :param min_capacity: The minimum number of Aurora Serverless V2 capacity units. Default: 0.5
        :param removal_policy: Controls what happens to the database if it stops being managed by CloudFormation. Default: RemovalPolicy.RETAIN
        :param single_db_instance: Whether to use single RDS instance rather than RDS cluster. Not recommended for production. Default: false
        '''
        if isinstance(database_subnets, dict):
            database_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**database_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f78744aaadc5e2b52b8b55307c52fad3d248fca25e2c7006a16585b6e1392475)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument aurora_serverless", value=aurora_serverless, expected_type=type_hints["aurora_serverless"])
            check_type(argname="argument aurora_serverless_v2", value=aurora_serverless_v2, expected_type=type_hints["aurora_serverless_v2"])
            check_type(argname="argument backup_retention", value=backup_retention, expected_type=type_hints["backup_retention"])
            check_type(argname="argument cluster_engine", value=cluster_engine, expected_type=type_hints["cluster_engine"])
            check_type(argname="argument database_subnets", value=database_subnets, expected_type=type_hints["database_subnets"])
            check_type(argname="argument instance_engine", value=instance_engine, expected_type=type_hints["instance_engine"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument max_capacity", value=max_capacity, expected_type=type_hints["max_capacity"])
            check_type(argname="argument min_capacity", value=min_capacity, expected_type=type_hints["min_capacity"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument single_db_instance", value=single_db_instance, expected_type=type_hints["single_db_instance"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc": vpc,
        }
        if aurora_serverless is not None:
            self._values["aurora_serverless"] = aurora_serverless
        if aurora_serverless_v2 is not None:
            self._values["aurora_serverless_v2"] = aurora_serverless_v2
        if backup_retention is not None:
            self._values["backup_retention"] = backup_retention
        if cluster_engine is not None:
            self._values["cluster_engine"] = cluster_engine
        if database_subnets is not None:
            self._values["database_subnets"] = database_subnets
        if instance_engine is not None:
            self._values["instance_engine"] = instance_engine
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if max_capacity is not None:
            self._values["max_capacity"] = max_capacity
        if min_capacity is not None:
            self._values["min_capacity"] = min_capacity
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if single_db_instance is not None:
            self._values["single_db_instance"] = single_db_instance

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The VPC for the database.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def aurora_serverless(self) -> typing.Optional[builtins.bool]:
        '''enable aurora serverless.

        :default: false
        '''
        result = self._values.get("aurora_serverless")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def aurora_serverless_v2(self) -> typing.Optional[builtins.bool]:
        '''enable aurora serverless v2.

        :default: false
        '''
        result = self._values.get("aurora_serverless_v2")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def backup_retention(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''database backup retension.

        :default: - 7 days
        '''
        result = self._values.get("backup_retention")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def cluster_engine(
        self,
    ) -> typing.Optional[_aws_cdk_aws_rds_ceddda9d.IClusterEngine]:
        '''The database cluster engine.

        :default: rds.AuroraMysqlEngineVersion.VER_2_09_1
        '''
        result = self._values.get("cluster_engine")
        return typing.cast(typing.Optional[_aws_cdk_aws_rds_ceddda9d.IClusterEngine], result)

    @builtins.property
    def database_subnets(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''VPC subnets for database.'''
        result = self._values.get("database_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def instance_engine(
        self,
    ) -> typing.Optional[_aws_cdk_aws_rds_ceddda9d.IInstanceEngine]:
        '''The database instance engine.

        :default: - MySQL 8.0.21
        '''
        result = self._values.get("instance_engine")
        return typing.cast(typing.Optional[_aws_cdk_aws_rds_ceddda9d.IInstanceEngine], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType]:
        '''The database instance type.

        :default: r5.large
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType], result)

    @builtins.property
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of Aurora Serverless V2 capacity units.

        :default: 10
        '''
        result = self._values.get("max_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_capacity(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of Aurora Serverless V2 capacity units.

        :default: 0.5
        '''
        result = self._values.get("min_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''Controls what happens to the database if it stops being managed by CloudFormation.

        :default: RemovalPolicy.RETAIN
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def single_db_instance(self) -> typing.Optional[builtins.bool]:
        '''Whether to use single RDS instance rather than RDS cluster.

        Not recommended for production.

        :default: false
        '''
        result = self._values.get("single_db_instance")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KeyCloak(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-keycloak.KeyCloak",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        certificate_arn: builtins.str,
        keycloak_version: "KeycloakVersion",
        aurora_serverless: typing.Optional[builtins.bool] = None,
        aurora_serverless_v2: typing.Optional[builtins.bool] = None,
        auto_scale_task: typing.Optional[typing.Union[AutoScaleTask, typing.Dict[builtins.str, typing.Any]]] = None,
        backup_retention: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        bastion: typing.Optional[builtins.bool] = None,
        cluster_engine: typing.Optional[_aws_cdk_aws_rds_ceddda9d.IClusterEngine] = None,
        container_image: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ContainerImage] = None,
        database_instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        database_max_capacity: typing.Optional[jsii.Number] = None,
        database_min_capacity: typing.Optional[jsii.Number] = None,
        database_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        database_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        hostname: typing.Optional[builtins.str] = None,
        instance_engine: typing.Optional[_aws_cdk_aws_rds_ceddda9d.IInstanceEngine] = None,
        internet_facing: typing.Optional[builtins.bool] = None,
        node_count: typing.Optional[jsii.Number] = None,
        private_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        public_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        single_db_instance: typing.Optional[builtins.bool] = None,
        stickiness_cookie_duration: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        task_cpu: typing.Optional[jsii.Number] = None,
        task_memory: typing.Optional[jsii.Number] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param certificate_arn: ACM certificate ARN to import.
        :param keycloak_version: The Keycloak version for the cluster.
        :param aurora_serverless: Whether to use aurora serverless. When enabled, the ``databaseInstanceType`` and ``engine`` will be ignored. The ``rds.DatabaseClusterEngine.AURORA_MYSQL`` will be used as the default cluster engine instead. Default: false
        :param aurora_serverless_v2: Whether to use aurora serverless v2. When enabled, the ``databaseInstanceType`` will be ignored. Default: false
        :param auto_scale_task: Autoscaling for the ECS Service. Default: - no ecs service autoscaling
        :param backup_retention: database backup retension. Default: - 7 days
        :param bastion: Create a bastion host for debugging or trouble-shooting. Default: false
        :param cluster_engine: The database cluster engine. Default: rds.AuroraMysqlEngineVersion.VER_2_09_1
        :param container_image: Overrides the default image. Default: quay.io/keycloak/keycloak:${KEYCLOAK_VERSION}
        :param database_instance_type: Database instance type. Default: r5.large
        :param database_max_capacity: The maximum number of Aurora Serverless V2 capacity units. Default: 10
        :param database_min_capacity: The minimum number of Aurora Serverless V2 capacity units. Default: 0.5
        :param database_removal_policy: Controls what happens to the database if it stops being managed by CloudFormation. Default: RemovalPolicy.RETAIN
        :param database_subnets: VPC subnets for database. Default: - VPC isolated subnets
        :param env: The environment variables to pass to the keycloak container.
        :param hostname: The hostname to use for the keycloak server.
        :param instance_engine: The database instance engine. Default: - MySQL 8.0.21
        :param internet_facing: Whether to put the load balancer in the public or private subnets. Default: true
        :param node_count: Number of keycloak node in the cluster. Default: 2
        :param private_subnets: VPC private subnets for keycloak service. Default: - VPC private subnets
        :param public_subnets: VPC public subnets for ALB. Default: - VPC public subnets
        :param single_db_instance: Whether to use single RDS instance rather than RDS cluster. Not recommended for production. Default: false
        :param stickiness_cookie_duration: The sticky session duration for the keycloak workload with ALB. Default: - one day
        :param task_cpu: The number of cpu units used by the keycloak task. Default: 4096
        :param task_memory: The amount (in MiB) of memory used by the keycloak task. Default: 8192
        :param vpc: VPC for the workload.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b241863734b5dade9c2af0e8b16d52c9acb38a04ed43957650734570f2027752)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = KeyCloakProps(
            certificate_arn=certificate_arn,
            keycloak_version=keycloak_version,
            aurora_serverless=aurora_serverless,
            aurora_serverless_v2=aurora_serverless_v2,
            auto_scale_task=auto_scale_task,
            backup_retention=backup_retention,
            bastion=bastion,
            cluster_engine=cluster_engine,
            container_image=container_image,
            database_instance_type=database_instance_type,
            database_max_capacity=database_max_capacity,
            database_min_capacity=database_min_capacity,
            database_removal_policy=database_removal_policy,
            database_subnets=database_subnets,
            env=env,
            hostname=hostname,
            instance_engine=instance_engine,
            internet_facing=internet_facing,
            node_count=node_count,
            private_subnets=private_subnets,
            public_subnets=public_subnets,
            single_db_instance=single_db_instance,
            stickiness_cookie_duration=stickiness_cookie_duration,
            task_cpu=task_cpu,
            task_memory=task_memory,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addDatabase")
    def add_database(
        self,
        *,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        aurora_serverless: typing.Optional[builtins.bool] = None,
        aurora_serverless_v2: typing.Optional[builtins.bool] = None,
        backup_retention: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        cluster_engine: typing.Optional[_aws_cdk_aws_rds_ceddda9d.IClusterEngine] = None,
        database_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        instance_engine: typing.Optional[_aws_cdk_aws_rds_ceddda9d.IInstanceEngine] = None,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        single_db_instance: typing.Optional[builtins.bool] = None,
    ) -> Database:
        '''
        :param vpc: The VPC for the database.
        :param aurora_serverless: enable aurora serverless. Default: false
        :param aurora_serverless_v2: enable aurora serverless v2. Default: false
        :param backup_retention: database backup retension. Default: - 7 days
        :param cluster_engine: The database cluster engine. Default: rds.AuroraMysqlEngineVersion.VER_2_09_1
        :param database_subnets: VPC subnets for database.
        :param instance_engine: The database instance engine. Default: - MySQL 8.0.21
        :param instance_type: The database instance type. Default: r5.large
        :param max_capacity: The maximum number of Aurora Serverless V2 capacity units. Default: 10
        :param min_capacity: The minimum number of Aurora Serverless V2 capacity units. Default: 0.5
        :param removal_policy: Controls what happens to the database if it stops being managed by CloudFormation. Default: RemovalPolicy.RETAIN
        :param single_db_instance: Whether to use single RDS instance rather than RDS cluster. Not recommended for production. Default: false
        '''
        props = DatabaseProps(
            vpc=vpc,
            aurora_serverless=aurora_serverless,
            aurora_serverless_v2=aurora_serverless_v2,
            backup_retention=backup_retention,
            cluster_engine=cluster_engine,
            database_subnets=database_subnets,
            instance_engine=instance_engine,
            instance_type=instance_type,
            max_capacity=max_capacity,
            min_capacity=min_capacity,
            removal_policy=removal_policy,
            single_db_instance=single_db_instance,
        )

        return typing.cast(Database, jsii.invoke(self, "addDatabase", [props]))

    @jsii.member(jsii_name="addKeyCloakContainerService")
    def add_key_cloak_container_service(
        self,
        *,
        certificate: _aws_cdk_aws_certificatemanager_ceddda9d.ICertificate,
        database: Database,
        keycloak_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        keycloak_version: "KeycloakVersion",
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        auto_scale_task: typing.Optional[typing.Union[AutoScaleTask, typing.Dict[builtins.str, typing.Any]]] = None,
        bastion: typing.Optional[builtins.bool] = None,
        circuit_breaker: typing.Optional[builtins.bool] = None,
        container_image: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ContainerImage] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        hostname: typing.Optional[builtins.str] = None,
        internet_facing: typing.Optional[builtins.bool] = None,
        node_count: typing.Optional[jsii.Number] = None,
        private_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        public_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        stickiness_cookie_duration: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        task_cpu: typing.Optional[jsii.Number] = None,
        task_memory: typing.Optional[jsii.Number] = None,
    ) -> ContainerService:
        '''
        :param certificate: The ACM certificate.
        :param database: The RDS database for the service.
        :param keycloak_secret: The secrets manager secret for the keycloak.
        :param keycloak_version: Keycloak version for the container image.
        :param vpc: The VPC for the service.
        :param auto_scale_task: Autoscaling for the ECS Service. Default: - no ecs service autoscaling
        :param bastion: Whether to create the bastion host. Default: false
        :param circuit_breaker: Whether to enable the ECS service deployment circuit breaker. Default: false
        :param container_image: Overrides the default image. Default: quay.io/keycloak/keycloak:${KEYCLOAK_VERSION}
        :param env: The environment variables to pass to the keycloak container.
        :param hostname: The hostname to use for the keycloak server.
        :param internet_facing: Whether to put the put the load balancer in the public or private subnets. Default: true
        :param node_count: Number of keycloak node in the cluster. Default: 1
        :param private_subnets: VPC subnets for keycloak service.
        :param public_subnets: VPC public subnets for ALB.
        :param stickiness_cookie_duration: The sticky session duration for the keycloak workload with ALB. Default: - one day
        :param task_cpu: The number of cpu units used by the keycloak task. Default: 4096
        :param task_memory: The amount (in MiB) of memory used by the keycloak task. Default: 8192
        '''
        props = ContainerServiceProps(
            certificate=certificate,
            database=database,
            keycloak_secret=keycloak_secret,
            keycloak_version=keycloak_version,
            vpc=vpc,
            auto_scale_task=auto_scale_task,
            bastion=bastion,
            circuit_breaker=circuit_breaker,
            container_image=container_image,
            env=env,
            hostname=hostname,
            internet_facing=internet_facing,
            node_count=node_count,
            private_subnets=private_subnets,
            public_subnets=public_subnets,
            stickiness_cookie_duration=stickiness_cookie_duration,
            task_cpu=task_cpu,
            task_memory=task_memory,
        )

        return typing.cast(ContainerService, jsii.invoke(self, "addKeyCloakContainerService", [props]))

    @builtins.property
    @jsii.member(jsii_name="applicationLoadBalancer")
    def application_load_balancer(
        self,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationLoadBalancer:
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationLoadBalancer, jsii.get(self, "applicationLoadBalancer"))

    @builtins.property
    @jsii.member(jsii_name="keycloakSecret")
    def keycloak_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, jsii.get(self, "keycloakSecret"))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, jsii.get(self, "vpc"))

    @builtins.property
    @jsii.member(jsii_name="db")
    def db(self) -> typing.Optional[Database]:
        return typing.cast(typing.Optional[Database], jsii.get(self, "db"))


@jsii.data_type(
    jsii_type="cdk-keycloak.KeyCloakProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_arn": "certificateArn",
        "keycloak_version": "keycloakVersion",
        "aurora_serverless": "auroraServerless",
        "aurora_serverless_v2": "auroraServerlessV2",
        "auto_scale_task": "autoScaleTask",
        "backup_retention": "backupRetention",
        "bastion": "bastion",
        "cluster_engine": "clusterEngine",
        "container_image": "containerImage",
        "database_instance_type": "databaseInstanceType",
        "database_max_capacity": "databaseMaxCapacity",
        "database_min_capacity": "databaseMinCapacity",
        "database_removal_policy": "databaseRemovalPolicy",
        "database_subnets": "databaseSubnets",
        "env": "env",
        "hostname": "hostname",
        "instance_engine": "instanceEngine",
        "internet_facing": "internetFacing",
        "node_count": "nodeCount",
        "private_subnets": "privateSubnets",
        "public_subnets": "publicSubnets",
        "single_db_instance": "singleDbInstance",
        "stickiness_cookie_duration": "stickinessCookieDuration",
        "task_cpu": "taskCpu",
        "task_memory": "taskMemory",
        "vpc": "vpc",
    },
)
class KeyCloakProps:
    def __init__(
        self,
        *,
        certificate_arn: builtins.str,
        keycloak_version: "KeycloakVersion",
        aurora_serverless: typing.Optional[builtins.bool] = None,
        aurora_serverless_v2: typing.Optional[builtins.bool] = None,
        auto_scale_task: typing.Optional[typing.Union[AutoScaleTask, typing.Dict[builtins.str, typing.Any]]] = None,
        backup_retention: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        bastion: typing.Optional[builtins.bool] = None,
        cluster_engine: typing.Optional[_aws_cdk_aws_rds_ceddda9d.IClusterEngine] = None,
        container_image: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ContainerImage] = None,
        database_instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        database_max_capacity: typing.Optional[jsii.Number] = None,
        database_min_capacity: typing.Optional[jsii.Number] = None,
        database_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        database_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        hostname: typing.Optional[builtins.str] = None,
        instance_engine: typing.Optional[_aws_cdk_aws_rds_ceddda9d.IInstanceEngine] = None,
        internet_facing: typing.Optional[builtins.bool] = None,
        node_count: typing.Optional[jsii.Number] = None,
        private_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        public_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        single_db_instance: typing.Optional[builtins.bool] = None,
        stickiness_cookie_duration: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        task_cpu: typing.Optional[jsii.Number] = None,
        task_memory: typing.Optional[jsii.Number] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''
        :param certificate_arn: ACM certificate ARN to import.
        :param keycloak_version: The Keycloak version for the cluster.
        :param aurora_serverless: Whether to use aurora serverless. When enabled, the ``databaseInstanceType`` and ``engine`` will be ignored. The ``rds.DatabaseClusterEngine.AURORA_MYSQL`` will be used as the default cluster engine instead. Default: false
        :param aurora_serverless_v2: Whether to use aurora serverless v2. When enabled, the ``databaseInstanceType`` will be ignored. Default: false
        :param auto_scale_task: Autoscaling for the ECS Service. Default: - no ecs service autoscaling
        :param backup_retention: database backup retension. Default: - 7 days
        :param bastion: Create a bastion host for debugging or trouble-shooting. Default: false
        :param cluster_engine: The database cluster engine. Default: rds.AuroraMysqlEngineVersion.VER_2_09_1
        :param container_image: Overrides the default image. Default: quay.io/keycloak/keycloak:${KEYCLOAK_VERSION}
        :param database_instance_type: Database instance type. Default: r5.large
        :param database_max_capacity: The maximum number of Aurora Serverless V2 capacity units. Default: 10
        :param database_min_capacity: The minimum number of Aurora Serverless V2 capacity units. Default: 0.5
        :param database_removal_policy: Controls what happens to the database if it stops being managed by CloudFormation. Default: RemovalPolicy.RETAIN
        :param database_subnets: VPC subnets for database. Default: - VPC isolated subnets
        :param env: The environment variables to pass to the keycloak container.
        :param hostname: The hostname to use for the keycloak server.
        :param instance_engine: The database instance engine. Default: - MySQL 8.0.21
        :param internet_facing: Whether to put the load balancer in the public or private subnets. Default: true
        :param node_count: Number of keycloak node in the cluster. Default: 2
        :param private_subnets: VPC private subnets for keycloak service. Default: - VPC private subnets
        :param public_subnets: VPC public subnets for ALB. Default: - VPC public subnets
        :param single_db_instance: Whether to use single RDS instance rather than RDS cluster. Not recommended for production. Default: false
        :param stickiness_cookie_duration: The sticky session duration for the keycloak workload with ALB. Default: - one day
        :param task_cpu: The number of cpu units used by the keycloak task. Default: 4096
        :param task_memory: The amount (in MiB) of memory used by the keycloak task. Default: 8192
        :param vpc: VPC for the workload.
        '''
        if isinstance(auto_scale_task, dict):
            auto_scale_task = AutoScaleTask(**auto_scale_task)
        if isinstance(database_subnets, dict):
            database_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**database_subnets)
        if isinstance(private_subnets, dict):
            private_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**private_subnets)
        if isinstance(public_subnets, dict):
            public_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**public_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7ef2eef0198e6aeb2a8305dfc49b52403c5f91deb5f0bcbe1f9482768bffa24)
            check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
            check_type(argname="argument keycloak_version", value=keycloak_version, expected_type=type_hints["keycloak_version"])
            check_type(argname="argument aurora_serverless", value=aurora_serverless, expected_type=type_hints["aurora_serverless"])
            check_type(argname="argument aurora_serverless_v2", value=aurora_serverless_v2, expected_type=type_hints["aurora_serverless_v2"])
            check_type(argname="argument auto_scale_task", value=auto_scale_task, expected_type=type_hints["auto_scale_task"])
            check_type(argname="argument backup_retention", value=backup_retention, expected_type=type_hints["backup_retention"])
            check_type(argname="argument bastion", value=bastion, expected_type=type_hints["bastion"])
            check_type(argname="argument cluster_engine", value=cluster_engine, expected_type=type_hints["cluster_engine"])
            check_type(argname="argument container_image", value=container_image, expected_type=type_hints["container_image"])
            check_type(argname="argument database_instance_type", value=database_instance_type, expected_type=type_hints["database_instance_type"])
            check_type(argname="argument database_max_capacity", value=database_max_capacity, expected_type=type_hints["database_max_capacity"])
            check_type(argname="argument database_min_capacity", value=database_min_capacity, expected_type=type_hints["database_min_capacity"])
            check_type(argname="argument database_removal_policy", value=database_removal_policy, expected_type=type_hints["database_removal_policy"])
            check_type(argname="argument database_subnets", value=database_subnets, expected_type=type_hints["database_subnets"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument instance_engine", value=instance_engine, expected_type=type_hints["instance_engine"])
            check_type(argname="argument internet_facing", value=internet_facing, expected_type=type_hints["internet_facing"])
            check_type(argname="argument node_count", value=node_count, expected_type=type_hints["node_count"])
            check_type(argname="argument private_subnets", value=private_subnets, expected_type=type_hints["private_subnets"])
            check_type(argname="argument public_subnets", value=public_subnets, expected_type=type_hints["public_subnets"])
            check_type(argname="argument single_db_instance", value=single_db_instance, expected_type=type_hints["single_db_instance"])
            check_type(argname="argument stickiness_cookie_duration", value=stickiness_cookie_duration, expected_type=type_hints["stickiness_cookie_duration"])
            check_type(argname="argument task_cpu", value=task_cpu, expected_type=type_hints["task_cpu"])
            check_type(argname="argument task_memory", value=task_memory, expected_type=type_hints["task_memory"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "certificate_arn": certificate_arn,
            "keycloak_version": keycloak_version,
        }
        if aurora_serverless is not None:
            self._values["aurora_serverless"] = aurora_serverless
        if aurora_serverless_v2 is not None:
            self._values["aurora_serverless_v2"] = aurora_serverless_v2
        if auto_scale_task is not None:
            self._values["auto_scale_task"] = auto_scale_task
        if backup_retention is not None:
            self._values["backup_retention"] = backup_retention
        if bastion is not None:
            self._values["bastion"] = bastion
        if cluster_engine is not None:
            self._values["cluster_engine"] = cluster_engine
        if container_image is not None:
            self._values["container_image"] = container_image
        if database_instance_type is not None:
            self._values["database_instance_type"] = database_instance_type
        if database_max_capacity is not None:
            self._values["database_max_capacity"] = database_max_capacity
        if database_min_capacity is not None:
            self._values["database_min_capacity"] = database_min_capacity
        if database_removal_policy is not None:
            self._values["database_removal_policy"] = database_removal_policy
        if database_subnets is not None:
            self._values["database_subnets"] = database_subnets
        if env is not None:
            self._values["env"] = env
        if hostname is not None:
            self._values["hostname"] = hostname
        if instance_engine is not None:
            self._values["instance_engine"] = instance_engine
        if internet_facing is not None:
            self._values["internet_facing"] = internet_facing
        if node_count is not None:
            self._values["node_count"] = node_count
        if private_subnets is not None:
            self._values["private_subnets"] = private_subnets
        if public_subnets is not None:
            self._values["public_subnets"] = public_subnets
        if single_db_instance is not None:
            self._values["single_db_instance"] = single_db_instance
        if stickiness_cookie_duration is not None:
            self._values["stickiness_cookie_duration"] = stickiness_cookie_duration
        if task_cpu is not None:
            self._values["task_cpu"] = task_cpu
        if task_memory is not None:
            self._values["task_memory"] = task_memory
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def certificate_arn(self) -> builtins.str:
        '''ACM certificate ARN to import.'''
        result = self._values.get("certificate_arn")
        assert result is not None, "Required property 'certificate_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def keycloak_version(self) -> "KeycloakVersion":
        '''The Keycloak version for the cluster.'''
        result = self._values.get("keycloak_version")
        assert result is not None, "Required property 'keycloak_version' is missing"
        return typing.cast("KeycloakVersion", result)

    @builtins.property
    def aurora_serverless(self) -> typing.Optional[builtins.bool]:
        '''Whether to use aurora serverless.

        When enabled, the ``databaseInstanceType`` and
        ``engine`` will be ignored. The ``rds.DatabaseClusterEngine.AURORA_MYSQL`` will be used as
        the default cluster engine instead.

        :default: false
        '''
        result = self._values.get("aurora_serverless")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def aurora_serverless_v2(self) -> typing.Optional[builtins.bool]:
        '''Whether to use aurora serverless v2.

        When enabled, the ``databaseInstanceType`` will be ignored.

        :default: false
        '''
        result = self._values.get("aurora_serverless_v2")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def auto_scale_task(self) -> typing.Optional[AutoScaleTask]:
        '''Autoscaling for the ECS Service.

        :default: - no ecs service autoscaling
        '''
        result = self._values.get("auto_scale_task")
        return typing.cast(typing.Optional[AutoScaleTask], result)

    @builtins.property
    def backup_retention(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''database backup retension.

        :default: - 7 days
        '''
        result = self._values.get("backup_retention")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def bastion(self) -> typing.Optional[builtins.bool]:
        '''Create a bastion host for debugging or trouble-shooting.

        :default: false
        '''
        result = self._values.get("bastion")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cluster_engine(
        self,
    ) -> typing.Optional[_aws_cdk_aws_rds_ceddda9d.IClusterEngine]:
        '''The database cluster engine.

        :default: rds.AuroraMysqlEngineVersion.VER_2_09_1
        '''
        result = self._values.get("cluster_engine")
        return typing.cast(typing.Optional[_aws_cdk_aws_rds_ceddda9d.IClusterEngine], result)

    @builtins.property
    def container_image(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ContainerImage]:
        '''Overrides the default image.

        :default: quay.io/keycloak/keycloak:${KEYCLOAK_VERSION}
        '''
        result = self._values.get("container_image")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ContainerImage], result)

    @builtins.property
    def database_instance_type(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType]:
        '''Database instance type.

        :default: r5.large
        '''
        result = self._values.get("database_instance_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType], result)

    @builtins.property
    def database_max_capacity(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of Aurora Serverless V2 capacity units.

        :default: 10
        '''
        result = self._values.get("database_max_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def database_min_capacity(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of Aurora Serverless V2 capacity units.

        :default: 0.5
        '''
        result = self._values.get("database_min_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def database_removal_policy(
        self,
    ) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''Controls what happens to the database if it stops being managed by CloudFormation.

        :default: RemovalPolicy.RETAIN
        '''
        result = self._values.get("database_removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def database_subnets(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''VPC subnets for database.

        :default: - VPC isolated subnets
        '''
        result = self._values.get("database_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The environment variables to pass to the keycloak container.'''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def hostname(self) -> typing.Optional[builtins.str]:
        '''The hostname to use for the keycloak server.'''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_engine(
        self,
    ) -> typing.Optional[_aws_cdk_aws_rds_ceddda9d.IInstanceEngine]:
        '''The database instance engine.

        :default: - MySQL 8.0.21
        '''
        result = self._values.get("instance_engine")
        return typing.cast(typing.Optional[_aws_cdk_aws_rds_ceddda9d.IInstanceEngine], result)

    @builtins.property
    def internet_facing(self) -> typing.Optional[builtins.bool]:
        '''Whether to put the load balancer in the public or private subnets.

        :default: true
        '''
        result = self._values.get("internet_facing")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def node_count(self) -> typing.Optional[jsii.Number]:
        '''Number of keycloak node in the cluster.

        :default: 2
        '''
        result = self._values.get("node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def private_subnets(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''VPC private subnets for keycloak service.

        :default: - VPC private subnets
        '''
        result = self._values.get("private_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def public_subnets(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''VPC public subnets for ALB.

        :default: - VPC public subnets
        '''
        result = self._values.get("public_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def single_db_instance(self) -> typing.Optional[builtins.bool]:
        '''Whether to use single RDS instance rather than RDS cluster.

        Not recommended for production.

        :default: false
        '''
        result = self._values.get("single_db_instance")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stickiness_cookie_duration(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The sticky session duration for the keycloak workload with ALB.

        :default: - one day
        '''
        result = self._values.get("stickiness_cookie_duration")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def task_cpu(self) -> typing.Optional[jsii.Number]:
        '''The number of cpu units used by the keycloak task.

        :default: 4096

        :see: FargateTaskDefinitionProps
        '''
        result = self._values.get("task_cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def task_memory(self) -> typing.Optional[jsii.Number]:
        '''The amount (in MiB) of memory used by the keycloak task.

        :default: 8192

        :see: FargateTaskDefinitionProps
        '''
        result = self._values.get("task_memory")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''VPC for the workload.'''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyCloakProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KeycloakVersion(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-keycloak.KeycloakVersion",
):
    '''Keycloak  version.'''

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, version: builtins.str) -> "KeycloakVersion":
        '''Custom cluster version.

        :param version: custom version number.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__914f98b27dd76ea7dda6f34ed7e43913d2387dae02ed62ed2087b9a455f72e0d)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        return typing.cast("KeycloakVersion", jsii.sinvoke(cls, "of", [version]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V12_0_4")
    def V12_0_4(cls) -> "KeycloakVersion":
        '''Keycloak version 12.0.4.'''
        return typing.cast("KeycloakVersion", jsii.sget(cls, "V12_0_4"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V15_0_0")
    def V15_0_0(cls) -> "KeycloakVersion":
        '''Keycloak version 15.0.0.'''
        return typing.cast("KeycloakVersion", jsii.sget(cls, "V15_0_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V15_0_1")
    def V15_0_1(cls) -> "KeycloakVersion":
        '''Keycloak version 15.0.1.'''
        return typing.cast("KeycloakVersion", jsii.sget(cls, "V15_0_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V15_0_2")
    def V15_0_2(cls) -> "KeycloakVersion":
        '''Keycloak version 15.0.2.'''
        return typing.cast("KeycloakVersion", jsii.sget(cls, "V15_0_2"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V16_1_1")
    def V16_1_1(cls) -> "KeycloakVersion":
        '''Keycloak version 16.1.1.'''
        return typing.cast("KeycloakVersion", jsii.sget(cls, "V16_1_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V17_0_1")
    def V17_0_1(cls) -> "KeycloakVersion":
        '''Keycloak version 17.0.1.'''
        return typing.cast("KeycloakVersion", jsii.sget(cls, "V17_0_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V18_0_3")
    def V18_0_3(cls) -> "KeycloakVersion":
        '''Keycloak version 18.0.2.'''
        return typing.cast("KeycloakVersion", jsii.sget(cls, "V18_0_3"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V19_0_3")
    def V19_0_3(cls) -> "KeycloakVersion":
        '''Keycloak version 19.0.3.'''
        return typing.cast("KeycloakVersion", jsii.sget(cls, "V19_0_3"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V20_0_3")
    def V20_0_3(cls) -> "KeycloakVersion":
        '''Keycloak version 20.0.5.'''
        return typing.cast("KeycloakVersion", jsii.sget(cls, "V20_0_3"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V21_0_0")
    def V21_0_0(cls) -> "KeycloakVersion":
        '''Keycloak version 21.0.0.'''
        return typing.cast("KeycloakVersion", jsii.sget(cls, "V21_0_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V21_0_1")
    def V21_0_1(cls) -> "KeycloakVersion":
        '''Keycloak version 21.0.1.'''
        return typing.cast("KeycloakVersion", jsii.sget(cls, "V21_0_1"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        '''cluster version number.'''
        return typing.cast(builtins.str, jsii.get(self, "version"))


__all__ = [
    "AutoScaleTask",
    "ContainerService",
    "ContainerServiceProps",
    "Database",
    "DatabaseConfig",
    "DatabaseProps",
    "KeyCloak",
    "KeyCloakProps",
    "KeycloakVersion",
]

publication.publish()

def _typecheckingstub__e3b0ccd8e2d54fa02d4baf3cc34671d011fbd811398e0fa7705a0176c146a0d4(
    *,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
    target_cpu_utilization: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0c2eef21e65e800e7034a8c9b53d89aa03dfe5a2dd0aa1ed8c3e20958b2e22d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    certificate: _aws_cdk_aws_certificatemanager_ceddda9d.ICertificate,
    database: Database,
    keycloak_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    keycloak_version: KeycloakVersion,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    auto_scale_task: typing.Optional[typing.Union[AutoScaleTask, typing.Dict[builtins.str, typing.Any]]] = None,
    bastion: typing.Optional[builtins.bool] = None,
    circuit_breaker: typing.Optional[builtins.bool] = None,
    container_image: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ContainerImage] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    hostname: typing.Optional[builtins.str] = None,
    internet_facing: typing.Optional[builtins.bool] = None,
    node_count: typing.Optional[jsii.Number] = None,
    private_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    public_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    stickiness_cookie_duration: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    task_cpu: typing.Optional[jsii.Number] = None,
    task_memory: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9423892d53ff57f474e07d6df4106ed0c077ac7a49f4d418a8e9c71ae627396e(
    *,
    certificate: _aws_cdk_aws_certificatemanager_ceddda9d.ICertificate,
    database: Database,
    keycloak_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    keycloak_version: KeycloakVersion,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    auto_scale_task: typing.Optional[typing.Union[AutoScaleTask, typing.Dict[builtins.str, typing.Any]]] = None,
    bastion: typing.Optional[builtins.bool] = None,
    circuit_breaker: typing.Optional[builtins.bool] = None,
    container_image: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ContainerImage] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    hostname: typing.Optional[builtins.str] = None,
    internet_facing: typing.Optional[builtins.bool] = None,
    node_count: typing.Optional[jsii.Number] = None,
    private_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    public_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    stickiness_cookie_duration: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    task_cpu: typing.Optional[jsii.Number] = None,
    task_memory: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__669d3357a4af4b4c29dded87b17f644277319118760adce20d6b09577165a6be(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    aurora_serverless: typing.Optional[builtins.bool] = None,
    aurora_serverless_v2: typing.Optional[builtins.bool] = None,
    backup_retention: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    cluster_engine: typing.Optional[_aws_cdk_aws_rds_ceddda9d.IClusterEngine] = None,
    database_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    instance_engine: typing.Optional[_aws_cdk_aws_rds_ceddda9d.IInstanceEngine] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    max_capacity: typing.Optional[jsii.Number] = None,
    min_capacity: typing.Optional[jsii.Number] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    single_db_instance: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dd52df53ef0f251d7b54810cc7cf33131743e97e18104fa376c9ff477e9be0a(
    *,
    connections: _aws_cdk_aws_ec2_ceddda9d.Connections,
    endpoint: builtins.str,
    identifier: builtins.str,
    secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f78744aaadc5e2b52b8b55307c52fad3d248fca25e2c7006a16585b6e1392475(
    *,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    aurora_serverless: typing.Optional[builtins.bool] = None,
    aurora_serverless_v2: typing.Optional[builtins.bool] = None,
    backup_retention: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    cluster_engine: typing.Optional[_aws_cdk_aws_rds_ceddda9d.IClusterEngine] = None,
    database_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    instance_engine: typing.Optional[_aws_cdk_aws_rds_ceddda9d.IInstanceEngine] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    max_capacity: typing.Optional[jsii.Number] = None,
    min_capacity: typing.Optional[jsii.Number] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    single_db_instance: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b241863734b5dade9c2af0e8b16d52c9acb38a04ed43957650734570f2027752(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    certificate_arn: builtins.str,
    keycloak_version: KeycloakVersion,
    aurora_serverless: typing.Optional[builtins.bool] = None,
    aurora_serverless_v2: typing.Optional[builtins.bool] = None,
    auto_scale_task: typing.Optional[typing.Union[AutoScaleTask, typing.Dict[builtins.str, typing.Any]]] = None,
    backup_retention: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    bastion: typing.Optional[builtins.bool] = None,
    cluster_engine: typing.Optional[_aws_cdk_aws_rds_ceddda9d.IClusterEngine] = None,
    container_image: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ContainerImage] = None,
    database_instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    database_max_capacity: typing.Optional[jsii.Number] = None,
    database_min_capacity: typing.Optional[jsii.Number] = None,
    database_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    database_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    hostname: typing.Optional[builtins.str] = None,
    instance_engine: typing.Optional[_aws_cdk_aws_rds_ceddda9d.IInstanceEngine] = None,
    internet_facing: typing.Optional[builtins.bool] = None,
    node_count: typing.Optional[jsii.Number] = None,
    private_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    public_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    single_db_instance: typing.Optional[builtins.bool] = None,
    stickiness_cookie_duration: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    task_cpu: typing.Optional[jsii.Number] = None,
    task_memory: typing.Optional[jsii.Number] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7ef2eef0198e6aeb2a8305dfc49b52403c5f91deb5f0bcbe1f9482768bffa24(
    *,
    certificate_arn: builtins.str,
    keycloak_version: KeycloakVersion,
    aurora_serverless: typing.Optional[builtins.bool] = None,
    aurora_serverless_v2: typing.Optional[builtins.bool] = None,
    auto_scale_task: typing.Optional[typing.Union[AutoScaleTask, typing.Dict[builtins.str, typing.Any]]] = None,
    backup_retention: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    bastion: typing.Optional[builtins.bool] = None,
    cluster_engine: typing.Optional[_aws_cdk_aws_rds_ceddda9d.IClusterEngine] = None,
    container_image: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ContainerImage] = None,
    database_instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    database_max_capacity: typing.Optional[jsii.Number] = None,
    database_min_capacity: typing.Optional[jsii.Number] = None,
    database_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    database_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    hostname: typing.Optional[builtins.str] = None,
    instance_engine: typing.Optional[_aws_cdk_aws_rds_ceddda9d.IInstanceEngine] = None,
    internet_facing: typing.Optional[builtins.bool] = None,
    node_count: typing.Optional[jsii.Number] = None,
    private_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    public_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    single_db_instance: typing.Optional[builtins.bool] = None,
    stickiness_cookie_duration: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    task_cpu: typing.Optional[jsii.Number] = None,
    task_memory: typing.Optional[jsii.Number] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__914f98b27dd76ea7dda6f34ed7e43913d2387dae02ed62ed2087b9a455f72e0d(
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
