'''
# cdk-vpc-module

cdk-vpc-module construct library is an open-source extension of the AWS Cloud Development Kit (AWS CDK) to deploy configurable aws vpc  and its individual components in less than 50 lines of code and human readable configuration which can be managed by pull requests!

## :sparkles: Features

* :white_check_mark: Option to configure custom IPv4 CIDR(10.10.0.0/24)
* :white_check_mark: VPC Peering with  route table entry
* :white_check_mark: Configurable NACL as per subnet group
* :white_check_mark: NATGateway as per availabilityZones

Using cdk a vpc can be deployed using the following sample code snippet:

```python
import { Network } from "@smallcase/cdk-vpc-module/lib/constructs/network";
import { aws_ec2 as ec2, App, Stack, StackProps } from "aws-cdk-lib";
import { Construct } from "constructs";

export class VPCStack extends Stack {
  constructor(scope: Construct, id: string, props: StackProps = {}) {
    super(scope, id, props);
    new Network(this, 'NETWORK', {
      vpc: {
        cidr: '10.10.0.0/16',
        subnetConfiguration: [],
      },
      peeringConfigs: {
        "TEST-PEERING": { // this key will be used as your peering id, which you will have to mention below when you configure a route table for your subnets
          peeringVpcId: "vpc-0000",
          tags: {
            "Name": "TEST-PEERING to CREATED-VPC",
            "Description": "Connect"
          }
        }
      },
      subnets: [
        {
          subnetGroupName: 'NATGateway',
          subnetType: ec2.SubnetType.PUBLIC,
          cidrBlock: ['10.10.0.0/28', '10.10.0.16/28', '10.10.0.32/28'],
          availabilityZones: ['ap-south-1a', 'ap-south-1b', 'ap-south-1c'],
          ingressNetworkACL: [
            {
              cidr: ec2.AclCidr.ipv4('0.0.0.0/0'),
              traffic: ec2.AclTraffic.allTraffic(),
            },
          ],
          routes: [
          ],
          egressNetworkACL: [
            {
              cidr: ec2.AclCidr.ipv4('0.0.0.0/0'),
              traffic: ec2.AclTraffic.allTraffic(),
            },
          ],
        },
        {
          subnetGroupName: 'Public',
          subnetType: ec2.SubnetType.PUBLIC,
          cidrBlock: ['10.10.2.0/24', '10.10.3.0/24', '10.10.4.0/24'],
          availabilityZones: ['ap-south-1a', 'ap-south-1b', 'ap-south-1c'],
          ingressNetworkACL: [
            {
              cidr: ec2.AclCidr.ipv4('0.0.0.0/0'),
              traffic: ec2.AclTraffic.allTraffic(),
            },
          ],
          egressNetworkACL: [
            {
              cidr: ec2.AclCidr.ipv4('0.0.0.0/0'),
              traffic: ec2.AclTraffic.allTraffic(),
            },
          ],
          routes: [
          ],
          tags: {
            // if you use this vpc for your eks cluster, you have to tag your subnets [read more](https://aws.amazon.com/premiumsupport/knowledge-center/eks-vpc-subnet-discovery/)
            'kubernetes.io/role/elb': '1',
            'kubernetes.io/cluster/TEST-CLUSTER': 'owned',
          },
        },
        {
          subnetGroupName: 'Private',
          subnetType: ec2.SubnetType.PRIVATE_WITH_NAT,
          cidrBlock: ['10.10.5.0/24', '10.10.6.0/24', '10.10.7.0/24'],
          availabilityZones: ['ap-south-1a', 'ap-south-1b', 'ap-south-1c'],
          ingressNetworkACL: [
            {
              cidr: ec2.AclCidr.ipv4('0.0.0.0/0'),
              traffic: ec2.AclTraffic.allTraffic(),
            },
          ],
          egressNetworkACL: [
            {
              cidr: ec2.AclCidr.ipv4('0.0.0.0/0'),
              traffic: ec2.AclTraffic.allTraffic(),
            },

          ],
          routes: [
            {
            // if you use this vpc for your eks cluster, you have to tag your subnets [read more](https://aws.amazon.com/premiumsupport/knowledge-center/eks-vpc-subnet-discovery/)
              routerType: ec2.RouterType.VPC_PEERING_CONNECTION,
              destinationCidrBlock: "<destinationCidrBlock>",
              //<Your VPC PeeringConfig KEY, in this example TEST-PEERING will be your ID>
              existingVpcPeeringRouteKey: "TEST-PEERING"
            }
          ],
          tags: {
            'kubernetes.io/role/internal-elb': '1',
            'kubernetes.io/cluster/TEST-CLUSTER': 'owned',
          },
        },
        {
          subnetGroupName: 'Database',
          subnetType: ec2.SubnetType.PRIVATE_WITH_NAT,
          cidrBlock: ['10.10.14.0/27', '10.10.14.32/27', '10.10.14.64/27'],
          availabilityZones: ['ap-south-1a', 'ap-south-1b', 'ap-south-1c'],
          ingressNetworkACL: [
            {
              cidr: ec2.AclCidr.ipv4('0.0.0.0/0'),
              traffic: ec2.AclTraffic.allTraffic(),
            },
          ],
          egressNetworkACL: [
            {
              cidr: ec2.AclCidr.ipv4('0.0.0.0/0'),
              traffic: ec2.AclTraffic.allTraffic(),
            },
          ],
          routes: [
          ],
          tags: {
          },
        },
      ],
    });
  }
}
const envDef = {
  account: '<AWS-ID>',
  region: '<AWS-REGION>',
};

const app = new App();

new VPCStack(app, 'TEST', {
  env: envDef,
  terminationProtection: true,
  tags: {
});
app.synth();
```

Please refer [here](/API.md) to check how to use individual resource constructs.

## :clapper: Quick Start

The quick start shows you how to create an **AWS-VPC** using this module.

### Prerequisites

* A working [`aws`](https://aws.amazon.com/cli/) CLI installation with access to an account and administrator privileges
* You'll need a recent [NodeJS](https://nodejs.org) installation

To get going you'll need a CDK project. For details please refer to the [detailed guide for CDK](https://docs.aws.amazon.com/cdk/latest/guide/hello_world.html).

Create an empty directory on your system.

```bash
mkdir aws-quick-start-vpc && cd aws-quick-start-vpc
```

Bootstrap your CDK project, we will use TypeScript, but you can switch to any other supported language.

```bash
npx cdk init sample-vpc  --language typescript
npx cdk bootstrap
```

Install using NPM:

```
npm install @smallcase/cdk-vpc-module
```

Using yarn

```
yarn add @smallcase/cdk-vpc-module
```

Check the changed which are to be deployed

```bash
~ -> npx cdk diff
```

Deploy using

```bash
~ -> npx cdk deploy
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

import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@smallcase/cdk-vpc-module.AddRouteOptions",
    jsii_struct_bases=[],
    name_mapping={
        "router_type": "routerType",
        "destination_cidr_block": "destinationCidrBlock",
        "destination_ipv6_cidr_block": "destinationIpv6CidrBlock",
        "enables_internet_connectivity": "enablesInternetConnectivity",
        "existing_vpc_peering_route_key": "existingVpcPeeringRouteKey",
        "router_id": "routerId",
    },
)
class AddRouteOptions:
    def __init__(
        self,
        *,
        router_type: _aws_cdk_aws_ec2_ceddda9d.RouterType,
        destination_cidr_block: typing.Optional[builtins.str] = None,
        destination_ipv6_cidr_block: typing.Optional[builtins.str] = None,
        enables_internet_connectivity: typing.Optional[builtins.bool] = None,
        existing_vpc_peering_route_key: typing.Optional[builtins.str] = None,
        router_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param router_type: What type of router to route this traffic to.
        :param destination_cidr_block: IPv4 range this route applies to. Default: '0.0.0.0/0'
        :param destination_ipv6_cidr_block: IPv6 range this route applies to. Default: - Uses IPv6
        :param enables_internet_connectivity: Whether this route will enable internet connectivity. If true, this route will be added before any AWS resources that depend on internet connectivity in the VPC will be created. Default: false
        :param existing_vpc_peering_route_key: 
        :param router_id: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77cff1a961dfe56849028f489d387bf7a42f4363289b43e3bab5a7a69aec3aa6)
            check_type(argname="argument router_type", value=router_type, expected_type=type_hints["router_type"])
            check_type(argname="argument destination_cidr_block", value=destination_cidr_block, expected_type=type_hints["destination_cidr_block"])
            check_type(argname="argument destination_ipv6_cidr_block", value=destination_ipv6_cidr_block, expected_type=type_hints["destination_ipv6_cidr_block"])
            check_type(argname="argument enables_internet_connectivity", value=enables_internet_connectivity, expected_type=type_hints["enables_internet_connectivity"])
            check_type(argname="argument existing_vpc_peering_route_key", value=existing_vpc_peering_route_key, expected_type=type_hints["existing_vpc_peering_route_key"])
            check_type(argname="argument router_id", value=router_id, expected_type=type_hints["router_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "router_type": router_type,
        }
        if destination_cidr_block is not None:
            self._values["destination_cidr_block"] = destination_cidr_block
        if destination_ipv6_cidr_block is not None:
            self._values["destination_ipv6_cidr_block"] = destination_ipv6_cidr_block
        if enables_internet_connectivity is not None:
            self._values["enables_internet_connectivity"] = enables_internet_connectivity
        if existing_vpc_peering_route_key is not None:
            self._values["existing_vpc_peering_route_key"] = existing_vpc_peering_route_key
        if router_id is not None:
            self._values["router_id"] = router_id

    @builtins.property
    def router_type(self) -> _aws_cdk_aws_ec2_ceddda9d.RouterType:
        '''What type of router to route this traffic to.'''
        result = self._values.get("router_type")
        assert result is not None, "Required property 'router_type' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.RouterType, result)

    @builtins.property
    def destination_cidr_block(self) -> typing.Optional[builtins.str]:
        '''IPv4 range this route applies to.

        :default: '0.0.0.0/0'
        '''
        result = self._values.get("destination_cidr_block")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_ipv6_cidr_block(self) -> typing.Optional[builtins.str]:
        '''IPv6 range this route applies to.

        :default: - Uses IPv6
        '''
        result = self._values.get("destination_ipv6_cidr_block")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enables_internet_connectivity(self) -> typing.Optional[builtins.bool]:
        '''Whether this route will enable internet connectivity.

        If true, this route will be added before any AWS resources that depend
        on internet connectivity in the VPC will be created.

        :default: false
        '''
        result = self._values.get("enables_internet_connectivity")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def existing_vpc_peering_route_key(self) -> typing.Optional[builtins.str]:
        result = self._values.get("existing_vpc_peering_route_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def router_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("router_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddRouteOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@smallcase/cdk-vpc-module.ISubnetsProps")
class ISubnetsProps(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.List[builtins.str]:
        ...

    @builtins.property
    @jsii.member(jsii_name="cidrBlock")
    def cidr_block(self) -> typing.List[builtins.str]:
        ...

    @builtins.property
    @jsii.member(jsii_name="subnetGroupName")
    def subnet_group_name(self) -> builtins.str:
        ...

    @builtins.property
    @jsii.member(jsii_name="subnetType")
    def subnet_type(self) -> _aws_cdk_aws_ec2_ceddda9d.SubnetType:
        ...

    @builtins.property
    @jsii.member(jsii_name="egressNetworkACL")
    def egress_network_acl(self) -> typing.Optional[typing.List["NetworkACL"]]:
        ...

    @builtins.property
    @jsii.member(jsii_name="ingressNetworkACL")
    def ingress_network_acl(self) -> typing.Optional[typing.List["NetworkACL"]]:
        ...

    @builtins.property
    @jsii.member(jsii_name="routes")
    def routes(self) -> typing.Optional[typing.List[AddRouteOptions]]:
        ...

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        ...

    @builtins.property
    @jsii.member(jsii_name="useSubnetForNAT")
    def use_subnet_for_nat(self) -> typing.Optional[builtins.bool]:
        ...


class _ISubnetsPropsProxy:
    __jsii_type__: typing.ClassVar[str] = "@smallcase/cdk-vpc-module.ISubnetsProps"

    @builtins.property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "availabilityZones"))

    @builtins.property
    @jsii.member(jsii_name="cidrBlock")
    def cidr_block(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "cidrBlock"))

    @builtins.property
    @jsii.member(jsii_name="subnetGroupName")
    def subnet_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetGroupName"))

    @builtins.property
    @jsii.member(jsii_name="subnetType")
    def subnet_type(self) -> _aws_cdk_aws_ec2_ceddda9d.SubnetType:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.SubnetType, jsii.get(self, "subnetType"))

    @builtins.property
    @jsii.member(jsii_name="egressNetworkACL")
    def egress_network_acl(self) -> typing.Optional[typing.List["NetworkACL"]]:
        return typing.cast(typing.Optional[typing.List["NetworkACL"]], jsii.get(self, "egressNetworkACL"))

    @builtins.property
    @jsii.member(jsii_name="ingressNetworkACL")
    def ingress_network_acl(self) -> typing.Optional[typing.List["NetworkACL"]]:
        return typing.cast(typing.Optional[typing.List["NetworkACL"]], jsii.get(self, "ingressNetworkACL"))

    @builtins.property
    @jsii.member(jsii_name="routes")
    def routes(self) -> typing.Optional[typing.List[AddRouteOptions]]:
        return typing.cast(typing.Optional[typing.List[AddRouteOptions]], jsii.get(self, "routes"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="useSubnetForNAT")
    def use_subnet_for_nat(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "useSubnetForNAT"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISubnetsProps).__jsii_proxy_class__ = lambda : _ISubnetsPropsProxy


class Network(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@smallcase/cdk-vpc-module.Network",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        subnets: typing.Sequence[ISubnetsProps],
        vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpcProps, typing.Dict[builtins.str, typing.Any]],
        nat_eip_allocation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        peering_configs: typing.Optional[typing.Mapping[builtins.str, typing.Union["PeeringConfig", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param subnets: 
        :param vpc: 
        :param nat_eip_allocation_ids: 
        :param peering_configs: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df3f88ed1cc891dbd636f210624927d010c33ac961e6f577806e2dd937c456be)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = VPCProps(
            subnets=subnets,
            vpc=vpc,
            nat_eip_allocation_ids=nat_eip_allocation_ids,
            peering_configs=peering_configs,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="createSubnet")
    def create_subnet(
        self,
        option: ISubnetsProps,
        vpc: _aws_cdk_aws_ec2_ceddda9d.Vpc,
    ) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.Subnet]:
        '''
        :param option: -
        :param vpc: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92666cd41c2c14d24ac75176f78720cccdba04127eb90a149be6f2fe21660cf1)
            check_type(argname="argument option", value=option, expected_type=type_hints["option"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        peering_connection_id = PeeringConnectionInternalType()

        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.Subnet], jsii.invoke(self, "createSubnet", [option, vpc, peering_connection_id]))

    @builtins.property
    @jsii.member(jsii_name="natProvider")
    def nat_provider(self) -> _aws_cdk_aws_ec2_ceddda9d.NatProvider:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.NatProvider, jsii.get(self, "natProvider"))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.Vpc:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Vpc, jsii.get(self, "vpc"))

    @builtins.property
    @jsii.member(jsii_name="natSubnets")
    def nat_subnets(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.PublicSubnet]:
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.PublicSubnet], jsii.get(self, "natSubnets"))

    @nat_subnets.setter
    def nat_subnets(
        self,
        value: typing.List[_aws_cdk_aws_ec2_ceddda9d.PublicSubnet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f78b8adef4396361d5c72de5dc0fba4922e4d9a7322c65f75ff8504d4bd76871)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "natSubnets", value)

    @builtins.property
    @jsii.member(jsii_name="pbSubnets")
    def pb_subnets(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.PublicSubnet]:
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.PublicSubnet], jsii.get(self, "pbSubnets"))

    @pb_subnets.setter
    def pb_subnets(
        self,
        value: typing.List[_aws_cdk_aws_ec2_ceddda9d.PublicSubnet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b69712fe7b2bc40ff22d1946b13d47d502e7bdb75a27de5e82a782f5b1e5ad06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pbSubnets", value)

    @builtins.property
    @jsii.member(jsii_name="pvSubnets")
    def pv_subnets(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.PrivateSubnet]:
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.PrivateSubnet], jsii.get(self, "pvSubnets"))

    @pv_subnets.setter
    def pv_subnets(
        self,
        value: typing.List[_aws_cdk_aws_ec2_ceddda9d.PrivateSubnet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5bfb10a99897571241006d792ce84acf324e915d0d0d7a70310260bbf97506a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pvSubnets", value)


@jsii.data_type(
    jsii_type="@smallcase/cdk-vpc-module.NetworkACL",
    jsii_struct_bases=[],
    name_mapping={"cidr": "cidr", "traffic": "traffic"},
)
class NetworkACL:
    def __init__(
        self,
        *,
        cidr: _aws_cdk_aws_ec2_ceddda9d.AclCidr,
        traffic: _aws_cdk_aws_ec2_ceddda9d.AclTraffic,
    ) -> None:
        '''
        :param cidr: 
        :param traffic: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a1970396c779835fc4afcade9ad3fdc707402f18a94acc262cf9e711955157f)
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            check_type(argname="argument traffic", value=traffic, expected_type=type_hints["traffic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cidr": cidr,
            "traffic": traffic,
        }

    @builtins.property
    def cidr(self) -> _aws_cdk_aws_ec2_ceddda9d.AclCidr:
        result = self._values.get("cidr")
        assert result is not None, "Required property 'cidr' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.AclCidr, result)

    @builtins.property
    def traffic(self) -> _aws_cdk_aws_ec2_ceddda9d.AclTraffic:
        result = self._values.get("traffic")
        assert result is not None, "Required property 'traffic' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.AclTraffic, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkACL(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/cdk-vpc-module.PeeringConfig",
    jsii_struct_bases=[],
    name_mapping={
        "peering_vpc_id": "peeringVpcId",
        "tags": "tags",
        "peer_assume_role_arn": "peerAssumeRoleArn",
        "peer_owner_id": "peerOwnerId",
        "peer_region": "peerRegion",
    },
)
class PeeringConfig:
    def __init__(
        self,
        *,
        peering_vpc_id: builtins.str,
        tags: typing.Mapping[builtins.str, builtins.str],
        peer_assume_role_arn: typing.Optional[builtins.str] = None,
        peer_owner_id: typing.Optional[builtins.str] = None,
        peer_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param peering_vpc_id: 
        :param tags: 
        :param peer_assume_role_arn: 
        :param peer_owner_id: 
        :param peer_region: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__906788234b850289efe7c3dfd41ad9a7598ad048a1820338c1962e640c00d246)
            check_type(argname="argument peering_vpc_id", value=peering_vpc_id, expected_type=type_hints["peering_vpc_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument peer_assume_role_arn", value=peer_assume_role_arn, expected_type=type_hints["peer_assume_role_arn"])
            check_type(argname="argument peer_owner_id", value=peer_owner_id, expected_type=type_hints["peer_owner_id"])
            check_type(argname="argument peer_region", value=peer_region, expected_type=type_hints["peer_region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "peering_vpc_id": peering_vpc_id,
            "tags": tags,
        }
        if peer_assume_role_arn is not None:
            self._values["peer_assume_role_arn"] = peer_assume_role_arn
        if peer_owner_id is not None:
            self._values["peer_owner_id"] = peer_owner_id
        if peer_region is not None:
            self._values["peer_region"] = peer_region

    @builtins.property
    def peering_vpc_id(self) -> builtins.str:
        result = self._values.get("peering_vpc_id")
        assert result is not None, "Required property 'peering_vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        result = self._values.get("tags")
        assert result is not None, "Required property 'tags' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def peer_assume_role_arn(self) -> typing.Optional[builtins.str]:
        result = self._values.get("peer_assume_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_owner_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("peer_owner_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_region(self) -> typing.Optional[builtins.str]:
        result = self._values.get("peer_region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PeeringConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/cdk-vpc-module.PeeringConnectionInternalType",
    jsii_struct_bases=[],
    name_mapping={},
)
class PeeringConnectionInternalType:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PeeringConnectionInternalType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/cdk-vpc-module.VPCProps",
    jsii_struct_bases=[],
    name_mapping={
        "subnets": "subnets",
        "vpc": "vpc",
        "nat_eip_allocation_ids": "natEipAllocationIds",
        "peering_configs": "peeringConfigs",
    },
)
class VPCProps:
    def __init__(
        self,
        *,
        subnets: typing.Sequence[ISubnetsProps],
        vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpcProps, typing.Dict[builtins.str, typing.Any]],
        nat_eip_allocation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        peering_configs: typing.Optional[typing.Mapping[builtins.str, typing.Union[PeeringConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param subnets: 
        :param vpc: 
        :param nat_eip_allocation_ids: 
        :param peering_configs: 
        '''
        if isinstance(vpc, dict):
            vpc = _aws_cdk_aws_ec2_ceddda9d.VpcProps(**vpc)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__276e14ede93619c8496d33625e8b9426df9db19c536b76f6785db1fff0434a40)
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument nat_eip_allocation_ids", value=nat_eip_allocation_ids, expected_type=type_hints["nat_eip_allocation_ids"])
            check_type(argname="argument peering_configs", value=peering_configs, expected_type=type_hints["peering_configs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subnets": subnets,
            "vpc": vpc,
        }
        if nat_eip_allocation_ids is not None:
            self._values["nat_eip_allocation_ids"] = nat_eip_allocation_ids
        if peering_configs is not None:
            self._values["peering_configs"] = peering_configs

    @builtins.property
    def subnets(self) -> typing.List[ISubnetsProps]:
        result = self._values.get("subnets")
        assert result is not None, "Required property 'subnets' is missing"
        return typing.cast(typing.List[ISubnetsProps], result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.VpcProps:
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.VpcProps, result)

    @builtins.property
    def nat_eip_allocation_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("nat_eip_allocation_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def peering_configs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, PeeringConfig]]:
        result = self._values.get("peering_configs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, PeeringConfig]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VPCProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AddRouteOptions",
    "ISubnetsProps",
    "Network",
    "NetworkACL",
    "PeeringConfig",
    "PeeringConnectionInternalType",
    "VPCProps",
]

publication.publish()

def _typecheckingstub__77cff1a961dfe56849028f489d387bf7a42f4363289b43e3bab5a7a69aec3aa6(
    *,
    router_type: _aws_cdk_aws_ec2_ceddda9d.RouterType,
    destination_cidr_block: typing.Optional[builtins.str] = None,
    destination_ipv6_cidr_block: typing.Optional[builtins.str] = None,
    enables_internet_connectivity: typing.Optional[builtins.bool] = None,
    existing_vpc_peering_route_key: typing.Optional[builtins.str] = None,
    router_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df3f88ed1cc891dbd636f210624927d010c33ac961e6f577806e2dd937c456be(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    subnets: typing.Sequence[ISubnetsProps],
    vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpcProps, typing.Dict[builtins.str, typing.Any]],
    nat_eip_allocation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    peering_configs: typing.Optional[typing.Mapping[builtins.str, typing.Union[PeeringConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92666cd41c2c14d24ac75176f78720cccdba04127eb90a149be6f2fe21660cf1(
    option: ISubnetsProps,
    vpc: _aws_cdk_aws_ec2_ceddda9d.Vpc,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f78b8adef4396361d5c72de5dc0fba4922e4d9a7322c65f75ff8504d4bd76871(
    value: typing.List[_aws_cdk_aws_ec2_ceddda9d.PublicSubnet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b69712fe7b2bc40ff22d1946b13d47d502e7bdb75a27de5e82a782f5b1e5ad06(
    value: typing.List[_aws_cdk_aws_ec2_ceddda9d.PublicSubnet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5bfb10a99897571241006d792ce84acf324e915d0d0d7a70310260bbf97506a(
    value: typing.List[_aws_cdk_aws_ec2_ceddda9d.PrivateSubnet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a1970396c779835fc4afcade9ad3fdc707402f18a94acc262cf9e711955157f(
    *,
    cidr: _aws_cdk_aws_ec2_ceddda9d.AclCidr,
    traffic: _aws_cdk_aws_ec2_ceddda9d.AclTraffic,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__906788234b850289efe7c3dfd41ad9a7598ad048a1820338c1962e640c00d246(
    *,
    peering_vpc_id: builtins.str,
    tags: typing.Mapping[builtins.str, builtins.str],
    peer_assume_role_arn: typing.Optional[builtins.str] = None,
    peer_owner_id: typing.Optional[builtins.str] = None,
    peer_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__276e14ede93619c8496d33625e8b9426df9db19c536b76f6785db1fff0434a40(
    *,
    subnets: typing.Sequence[ISubnetsProps],
    vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpcProps, typing.Dict[builtins.str, typing.Any]],
    nat_eip_allocation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    peering_configs: typing.Optional[typing.Mapping[builtins.str, typing.Union[PeeringConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
