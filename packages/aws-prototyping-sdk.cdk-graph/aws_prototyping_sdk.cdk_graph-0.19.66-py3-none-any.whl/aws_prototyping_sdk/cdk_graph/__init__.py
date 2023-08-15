'''
## CDK Graph (`@aws-prototyping-sdk/cdk-graph`)

![experimental](https://img.shields.io/badge/stability-experimental-orange.svg)
![alpha](https://img.shields.io/badge/version-alpha-red.svg)
[![API Documetnation](https://img.shields.io/badge/view-API_Documentation-blue.svg)](https://aws.github.io/aws-prototyping-sdk/typescript/cdk-graph/index.html)
[![Source Code](https://img.shields.io/badge/view-Source_Code-blue.svg)](https://github.com/aws/aws-prototyping-sdk/tree/mainline/packages/cdk-graph)

> More comprehensive documentation to come as this package stabilizes

This package is the core framework for supporting additional cdk based automation and tooling, such as diagraming, cost modeling, security and compliance, in a holistic and comprehensive way.

This package provides the following functionality:

1. Synthesizes a serialized graph (nodes and edges) from CDK source code.
2. Provides runtime interface for interacting with the graph (in-memory database-like graph store).
3. Provides plugin framework for additional tooling to utilize and extend the graph.

The goal of this framework is to enable bespoke tooling to be built without having to first traverse the CDK Tree and Metadata to build a graph. Projects like [cdk-dia](https://github.com/pistazie/cdk-dia) generate a bespoke in-memory graph that is then utilized to generate diagrams; while the diagram generation is the core value it must first have a graph to act upon and currently is required to generate this undifferentiated graph to provide its diagrams. By standardizing on the graph interface necessary to build complex tooling, we can more rapidly build new tooling that focuses on its core value.

---


### Available Plugins

| Name | Description | Screenshot | Links |
|--- | --- | --- | --- |
| **Diagram** | Generate cloud infrastructure diagrams from cdk graph | <img src="https://github.com/aws/aws-prototyping-sdk/blob/mainline/packages/cdk-graph-plugin-diagram/docs/examples/default.png?raw=true" style="max-width:200px;max-height:200px" /> | [![API Documetnation](https://img.shields.io/badge/view-API_Documentation-blue.svg)](https://aws.github.io/aws-prototyping-sdk/typescript/cdk-graph/index.html) [![Source Code](https://img.shields.io/badge/view-Source_Code-blue.svg)](https://github.com/aws/aws-prototyping-sdk/tree/mainline/packages/cdk-graph) |

---


### Quick Start

#### Instrument CDK App with CdkGraph

```python
#!/usr/bin/env node
import * as cdk from "aws-cdk-lib";
import { MyStack } from "../lib/my-stack";

import { CdkGraph } from "@aws-prototyping-sdk/cdk-graph";

const app = new cdk.App();
new MyStack(app, "MyStack");

// Add CdkGraph after other construct added to app
new CdkGraph(app);
```

#### Using Plugins

```python
#!/usr/bin/env node
import * as cdk from "aws-cdk-lib";
import { MyStack } from "../lib/my-stack";

import { CdkGraph } from "@aws-prototyping-sdk/cdk-graph";
import { ExamplePlugin } from "@aws-prototyping-sdk/cdk-graph-plugin-example"; // does not exist, just example

const app = new cdk.App();
new MyStack(app, "MyStack");

// Add CdkGraph after other construct added to app
new CdkGraph(app, {
  plugins: [new ExamplePlugin()],
});
```

---


### Config

Configuration is supported through the `.cdkgraphrc.js` and depending on the plugin, through passing config to the plugin instance.

Config precedence follows 1) defaults, 2) cdkgraphrc, 3) instance.

```js
// .cdkgraphrc.js
module.exports = {
  // Defaults to "<cdk.out>/cdkgraph"
  outdir: "reports/graph",

  // plugin configuration
  example: {
    verbose: true,
    reportType: "csv",
  },
};
```

```python
#!/usr/bin/env node
import * as cdk from "aws-cdk-lib";
import { MyStack } from "../lib/my-stack";

import { CdkGraph } from "@aws-prototyping-sdk/cdk-graph";
import { ExamplePlugin } from "@aws-prototyping-sdk/cdk-graph-plugin-example"; // does not exist, just example

const app = new cdk.App();
new MyStack(app, "MyStack");

// Add CdkGraph after other construct added to app
new CdkGraph(app, {
  plugins: [
    new ExamplePlugin({
      // Will override .cdkgraphrc.js value
      verbose: false,
    }),
  ],
});
```

---


### Plugin Interface

```python
/** CdkGraph **Plugin** interface */
export interface ICdkGraphPlugin {
  /** Unique identifier for this plugin */
  readonly id: string;
  /** Plugin version */
  readonly version: Version;
  /** List of plugins this plugin depends on, including optional semver version (eg: ["foo", "bar@1.2"]) */
  readonly dependencies?: string[];

  /**
   * Binds the plugin to the CdkGraph instance. Enables plugins to receive base configs.
   */
  bind: IGraphPluginBindCallback;

  /**
   * Node visitor callback for construct tree traversal. This follows IAspect.visit pattern, but the order
   * of visitor traversal in managed by the CdkGraph.
   */
  inspect?: IGraphVisitorCallback;
  /**
   * Called during CDK synthesize to generate synchronous artifacts based on the in-memory graph passed
   * to the plugin. This is called in fifo order of plugins.
   */
  synthesize?: IGraphSynthesizeCallback;
  /**
   * Generate asynchronous reports based on the graph. This is not automatically called when synthesizing CDK.
   * Developer must explicitly add `await graphInstance.report()` to the CDK bin or invoke this outside
   * of the CDK synth. In either case, the plugin receives the in-memory graph interface when invoked, as the
   * CdkGraph will deserialize the graph prior to invoking the plugin report.
   */
  report?: IGraphReportCallback;
}
```

Plugin operations are automatically invoked by CdkGraph in the order they are defined in the `plugins` property. The invocation flow of plugins follows: 1) `bind`, 2) `inspect`, 3) `synthesize`, 4) `async report`.

### Asynchronous Plugins

Some plugins may requiring performing asynchronous requests, or may make expensive operations that are best left outside of the synthesis process.

CdkGraph support asynchronous operations through the `async report()` method of plugins. However, since CDK does not support asynchronous operations during synthesis, this must be wired up a bit differently.

```python
#!/usr/bin/env node
import * as cdk from "aws-cdk-lib";
import { MyStack } from "../lib/my-stack";

import { CdkGraph } from "@aws-prototyping-sdk/cdk-graph";
import { ExampleAsyncPlugin } from "@aws-prototyping-sdk/cdk-graph-plugin-async-example"; // does not exist, just example

(async () => {
  const app = new cdk.App();
  new MyStack(app, "MyStack");

  // Add CdkGraph after other construct added to app
  const graph = new CdkGraph(app, {
    plugins: [new ExampleAsyncPlugin()],
  });

  // invokes all plugin `report()` operations asynchronously (in order they are defined in `plugins` property)
  await graph.report();
})();
```

### Example Plugin Implementation

Very basic example of implementing a plugin. Once the first actual plugins have been published this will be updated to reference those as examples.

```python
import {
  CdkGraph,
  CdkGraphContext,
  ICdkGraphPlugin,
} from "@aws-prototyping-sdk/cdk-graph";

export class CdkGraphExamplePlugin implements ICdkGraphPlugin {
  static readonly ARTIFACT_NS = "EXAMPLE";
  static readonly ID = "example";
  static readonly VERSION = "0.0.0";

  get id(): string {
    return CdkGraphDiagramPlugin.ID;
  }
  get version(): string {
    return CdkGraphDiagramPlugin.VERSION;
  }

  readonly dependencies?: string[] = [];

  /** @internal */
  private _graph?: CdkGraph;

  bind(graph: CdkGraph): void {
    this._graph = graph;
  }

  synthesize(context: CdkGraphContext): void {
    const pluginConfig = this.config as Required<IPluginConfig>;

    // Get counts of all resources
    const cfnResourceCounts = context.store.counts.cfnResources;

    // Write plugin artifact
    context.writeArtifact(
      this,
      "EXAMPLE",
      "example.json",
      JSON.stringify(cfnResourceCounts, null, 2)
    );
  }

  async report(context: CdkGraphContext): void {
    // perform async operation here utilizing graph store
    const cfnResourceCounts = context.store.counts.cfnResources;
    const fetchedData = await fetch("https://example.com/data", {
      method: "POST",
      body: JSON.stringify(cfnResourceCounts),
    });

    // Write plugin artifact for fetched data
    context.writeArtifact(
      this,
      "EXAMPLE:FETCHED",
      "example-fetched.json",
      JSON.stringify(fetchedData, null, 2)
    );
  }
}
```

### Path to Stability

The below is a rough checklist of task necessary to elevate this from experimental to stable.

* [ ] Dynamic versioning and Semver enforcement (store, plugins, etc)
* [ ] Support running `async report()` method outside of CDK synthesis process
* [ ] Find alternative synthesis solution that doesn't utilize CDK internals
* [ ] Support custom Nodes and Edges
* [ ] Improve logging, bookkeeping, and debugging
* [ ] Implement store upgrade solution
* [ ] Battle test the implementation against several plugins
* [ ] Battle test the implementation in all target languages (currently tested in Typescript, but vended in all PDK supported languages)
* [ ] Receive community feedback to validate approach
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

import constructs as _constructs_77d1e7e8


@jsii.enum(jsii_type="@aws-prototyping-sdk/cdk-graph.CdkConstructIds")
class CdkConstructIds(enum.Enum):
    '''(experimental) Common cdk construct ids.

    :stability: experimental
    '''

    DEFAULT = "DEFAULT"
    '''
    :stability: experimental
    '''
    RESOURCE = "RESOURCE"
    '''
    :stability: experimental
    '''
    EXPORTS = "EXPORTS"
    '''
    :stability: experimental
    '''


class CdkGraph(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-prototyping-sdk/cdk-graph.CdkGraph",
):
    '''(experimental) CdkGraph construct is the cdk-graph framework controller that is responsible for computing the graph, storing serialized graph, and instrumenting plugins per the plugin contract.

    :stability: experimental
    '''

    def __init__(
        self,
        root: _constructs_77d1e7e8.Construct,
        *,
        plugins: typing.Optional[typing.Sequence["ICdkGraphPlugin"]] = None,
    ) -> None:
        '''
        :param root: -
        :param plugins: (experimental) List of plugins to extends the graph. Plugins are invoked at each phases in fifo order.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28286f53bba3c64713566007568503857222212a302b0e060ba6e0b0d67633d0)
            check_type(argname="argument root", value=root, expected_type=type_hints["root"])
        props = ICdkGraphProps(plugins=plugins)

        jsii.create(self.__class__, self, [root, props])

    @jsii.member(jsii_name="report")
    def report(self) -> None:
        '''(experimental) Asynchronous report generation. This operation enables running expensive and non-synchronous report generation by plugins post synthesis.

        If a given plugin requires performing asynchronous operations or is general expensive, it should
        utilize ``report`` rather than ``synthesize``.

        :stability: experimental
        '''
        return typing.cast(None, jsii.ainvoke(self, "report", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ID")
    def ID(cls) -> builtins.str:
        '''(experimental) Fixed CdkGraph construct id.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ID"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="VERSION")
    def VERSION(cls) -> builtins.str:
        '''(experimental) Current CdkGraph semantic version.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "VERSION"))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''(experimental) Config.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="plugins")
    def plugins(self) -> typing.List["ICdkGraphPlugin"]:
        '''(experimental) List of plugins registered with this instance.

        :stability: experimental
        '''
        return typing.cast(typing.List["ICdkGraphPlugin"], jsii.get(self, "plugins"))

    @builtins.property
    @jsii.member(jsii_name="root")
    def root(self) -> _constructs_77d1e7e8.Construct:
        '''
        :stability: experimental
        '''
        return typing.cast(_constructs_77d1e7e8.Construct, jsii.get(self, "root"))

    @builtins.property
    @jsii.member(jsii_name="graphContext")
    def graph_context(self) -> typing.Optional["CdkGraphContext"]:
        '''(experimental) Get the context for the graph instance.

        This will be ``undefined`` before construct synthesis has initiated.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["CdkGraphContext"], jsii.get(self, "graphContext"))


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/cdk-graph.CdkGraphArtifact",
    jsii_struct_bases=[],
    name_mapping={
        "filename": "filename",
        "filepath": "filepath",
        "id": "id",
        "source": "source",
        "description": "description",
    },
)
class CdkGraphArtifact:
    def __init__(
        self,
        *,
        filename: builtins.str,
        filepath: builtins.str,
        id: builtins.str,
        source: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) CdkGraph artifact definition.

        :param filename: (experimental) Filename of the artifact.
        :param filepath: (experimental) Full path where artifact is stored.
        :param id: (experimental) The unique type of the artifact.
        :param source: (experimental) The source of the artifact (such as plugin, or core system, etc).
        :param description: (experimental) Description of artifact.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23a3bf1400984efa0d22219618f9f7c2b1b3cf1e07948dc134f293b4b7c2799d)
            check_type(argname="argument filename", value=filename, expected_type=type_hints["filename"])
            check_type(argname="argument filepath", value=filepath, expected_type=type_hints["filepath"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filename": filename,
            "filepath": filepath,
            "id": id,
            "source": source,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def filename(self) -> builtins.str:
        '''(experimental) Filename of the artifact.

        :stability: experimental
        '''
        result = self._values.get("filename")
        assert result is not None, "Required property 'filename' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filepath(self) -> builtins.str:
        '''(experimental) Full path where artifact is stored.

        :stability: experimental
        '''
        result = self._values.get("filepath")
        assert result is not None, "Required property 'filepath' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''(experimental) The unique type of the artifact.

        :stability: experimental
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> builtins.str:
        '''(experimental) The source of the artifact (such as plugin, or core system, etc).

        :stability: experimental
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description of artifact.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdkGraphArtifact(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-prototyping-sdk/cdk-graph.CdkGraphArtifacts")
class CdkGraphArtifacts(enum.Enum):
    '''(experimental) CdkGraph core artifacts.

    :stability: experimental
    '''

    GRAPH_METADATA = "GRAPH_METADATA"
    '''
    :stability: experimental
    '''
    GRAPH = "GRAPH"
    '''
    :stability: experimental
    '''


class CdkGraphContext(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-prototyping-sdk/cdk-graph.CdkGraphContext",
):
    '''(experimental) CdkGraph context.

    :stability: experimental
    '''

    def __init__(self, store: "Store", outdir: builtins.str) -> None:
        '''
        :param store: -
        :param outdir: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__989da9e5b172457303b3aef4ed9ac17f179950db8e46d91724cfbd2bef74748c)
            check_type(argname="argument store", value=store, expected_type=type_hints["store"])
            check_type(argname="argument outdir", value=outdir, expected_type=type_hints["outdir"])
        jsii.create(self.__class__, self, [store, outdir])

    @jsii.member(jsii_name="getArtifact")
    def get_artifact(self, id: builtins.str) -> CdkGraphArtifact:
        '''(experimental) Get CdkGraph artifact by id.

        :param id: -

        :stability: experimental
        :throws: Error is artifact does not exist
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__816d6f7e514bec099b526e77f33ac86bf42b1f7c17752bd722a51497ead76673)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast(CdkGraphArtifact, jsii.invoke(self, "getArtifact", [id]))

    @jsii.member(jsii_name="hasArtifactFile")
    def has_artifact_file(self, filename: builtins.str) -> builtins.bool:
        '''(experimental) Indicates if context has an artifact with *filename* defined.

        :param filename: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1a00986a437e5e797c994f6208b3c343e30d18bbaace95f147963e9d81cadaa)
            check_type(argname="argument filename", value=filename, expected_type=type_hints["filename"])
        return typing.cast(builtins.bool, jsii.invoke(self, "hasArtifactFile", [filename]))

    @jsii.member(jsii_name="logArtifact")
    def log_artifact(
        self,
        source: typing.Union[CdkGraph, "ICdkGraphPlugin"],
        id: builtins.str,
        filepath: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> CdkGraphArtifact:
        '''(experimental) Logs an artifact entry.

        In general this should not be called directly, as ``writeArtifact`` should be utilized
        to perform writing and logging artifacts. However some plugins utilize other tools that generate the artifacts,
        in which case the plugin would call this method to log the entry.

        :param source: The source of the artifact, such as the name of plugin.
        :param id: Unique id of the artifact.
        :param filepath: Full path where the artifact is stored.
        :param description: Description of the artifact.

        :stability: experimental
        :throws: Error is artifact id or filename already exists
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7076e52c64c67503ac32339aed9bc664c32f9a2ddb2e991c39310e6ef95f54e)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument filepath", value=filepath, expected_type=type_hints["filepath"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        return typing.cast(CdkGraphArtifact, jsii.invoke(self, "logArtifact", [source, id, filepath, description]))

    @jsii.member(jsii_name="writeArtifact")
    def write_artifact(
        self,
        source: typing.Union[CdkGraph, "ICdkGraphPlugin"],
        id: builtins.str,
        filename: builtins.str,
        data: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> CdkGraphArtifact:
        '''(experimental) Writes artifact data to outdir and logs the entry.

        :param source: The source of the artifact, such as the name of plugin.
        :param id: Unique id of the artifact.
        :param filename: Relative name of the file.
        :param data: -
        :param description: Description of the artifact.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46503812b23f70feadc9d32271563a9cd498878137bf496eb61bc3691922e6e9)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument filename", value=filename, expected_type=type_hints["filename"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        return typing.cast(CdkGraphArtifact, jsii.invoke(self, "writeArtifact", [source, id, filename, data, description]))

    @builtins.property
    @jsii.member(jsii_name="artifacts")
    def artifacts(self) -> typing.Mapping[builtins.str, CdkGraphArtifact]:
        '''(experimental) Get record of all graph artifacts keyed by artifact id.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, CdkGraphArtifact], jsii.get(self, "artifacts"))

    @builtins.property
    @jsii.member(jsii_name="graphJson")
    def graph_json(self) -> CdkGraphArtifact:
        '''(experimental) Get CdkGraph core ``graph.json`` artifact.

        :stability: experimental
        '''
        return typing.cast(CdkGraphArtifact, jsii.get(self, "graphJson"))

    @builtins.property
    @jsii.member(jsii_name="outdir")
    def outdir(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "outdir"))

    @builtins.property
    @jsii.member(jsii_name="store")
    def store(self) -> "Store":
        '''
        :stability: experimental
        '''
        return typing.cast("Store", jsii.get(self, "store"))


@jsii.enum(jsii_type="@aws-prototyping-sdk/cdk-graph.CfnAttributesEnum")
class CfnAttributesEnum(enum.Enum):
    '''(experimental) Common cfn attribute keys.

    :stability: experimental
    '''

    TYPE = "TYPE"
    '''
    :stability: experimental
    '''
    PROPS = "PROPS"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/cdk-graph.ConstructInfo",
    jsii_struct_bases=[],
    name_mapping={"fqn": "fqn", "version": "version"},
)
class ConstructInfo:
    def __init__(self, *, fqn: builtins.str, version: builtins.str) -> None:
        '''(experimental) Source information on a construct (class fqn and version).

        :param fqn: 
        :param version: 

        :see: https://github.com/aws/aws-cdk/blob/cea1039e3664fdfa89c6f00cdaeb1a0185a12678/packages/%40aws-cdk/core/lib/private/runtime-info.ts#L22
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0075161e9afebef046d274d60dcc85233e4fdd2bc46a8916a19dd21ded5d2e1a)
            check_type(argname="argument fqn", value=fqn, expected_type=type_hints["fqn"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fqn": fqn,
            "version": version,
        }

    @builtins.property
    def fqn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("fqn")
        assert result is not None, "Required property 'fqn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConstructInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-prototyping-sdk/cdk-graph.ConstructInfoFqnEnum")
class ConstructInfoFqnEnum(enum.Enum):
    '''(experimental) Commonly used cdk construct info fqn (jsii fully-qualified ids).

    :stability: experimental
    '''

    APP = "APP"
    '''
    :stability: experimental
    '''
    PDKAPP_MONO = "PDKAPP_MONO"
    '''
    :stability: experimental
    '''
    PDKAPP = "PDKAPP"
    '''
    :stability: experimental
    '''
    STAGE = "STAGE"
    '''
    :stability: experimental
    '''
    STACK = "STACK"
    '''
    :stability: experimental
    '''
    NESTED_STACK = "NESTED_STACK"
    '''
    :stability: experimental
    '''
    CFN_STACK = "CFN_STACK"
    '''
    :stability: experimental
    '''
    CFN_OUTPUT = "CFN_OUTPUT"
    '''
    :stability: experimental
    '''
    CFN_PARAMETER = "CFN_PARAMETER"
    '''
    :stability: experimental
    '''
    CUSTOM_RESOURCE = "CUSTOM_RESOURCE"
    '''
    :stability: experimental
    '''
    AWS_CUSTOM_RESOURCE = "AWS_CUSTOM_RESOURCE"
    '''
    :stability: experimental
    '''
    CUSTOM_RESOURCE_PROVIDER = "CUSTOM_RESOURCE_PROVIDER"
    '''
    :stability: experimental
    '''
    CUSTOM_RESOURCE_PROVIDER_2 = "CUSTOM_RESOURCE_PROVIDER_2"
    '''
    :stability: experimental
    '''
    LAMBDA = "LAMBDA"
    '''
    :stability: experimental
    '''
    CFN_LAMBDA = "CFN_LAMBDA"
    '''
    :stability: experimental
    '''
    LAMBDA_LAYER_VERSION = "LAMBDA_LAYER_VERSION"
    '''
    :stability: experimental
    '''
    CFN_LAMBDA_LAYER_VERSION = "CFN_LAMBDA_LAYER_VERSION"
    '''
    :stability: experimental
    '''
    LAMBDA_ALIAS = "LAMBDA_ALIAS"
    '''
    :stability: experimental
    '''
    CFN_LAMBDA_ALIAS = "CFN_LAMBDA_ALIAS"
    '''
    :stability: experimental
    '''
    LAMBDA_BASE = "LAMBDA_BASE"
    '''
    :stability: experimental
    '''
    LAMBDA_SINGLETON = "LAMBDA_SINGLETON"
    '''
    :stability: experimental
    '''
    LAMBDA_LAYER_AWSCLI = "LAMBDA_LAYER_AWSCLI"
    '''
    :stability: experimental
    '''
    CFN_LAMBDA_PERMISSIONS = "CFN_LAMBDA_PERMISSIONS"
    '''
    :stability: experimental
    '''
    ASSET_STAGING = "ASSET_STAGING"
    '''
    :stability: experimental
    '''
    S3_ASSET = "S3_ASSET"
    '''
    :stability: experimental
    '''
    ECR_TARBALL_ASSET = "ECR_TARBALL_ASSET"
    '''
    :stability: experimental
    '''
    EC2_INSTANCE = "EC2_INSTANCE"
    '''
    :stability: experimental
    '''
    CFN_EC2_INSTANCE = "CFN_EC2_INSTANCE"
    '''
    :stability: experimental
    '''
    SECURITY_GROUP = "SECURITY_GROUP"
    '''
    :stability: experimental
    '''
    CFN_SECURITY_GROUP = "CFN_SECURITY_GROUP"
    '''
    :stability: experimental
    '''
    VPC = "VPC"
    '''
    :stability: experimental
    '''
    CFN_VPC = "CFN_VPC"
    '''
    :stability: experimental
    '''
    PRIVATE_SUBNET = "PRIVATE_SUBNET"
    '''
    :stability: experimental
    '''
    CFN_PRIVATE_SUBNET = "CFN_PRIVATE_SUBNET"
    '''
    :stability: experimental
    '''
    PUBLIC_SUBNET = "PUBLIC_SUBNET"
    '''
    :stability: experimental
    '''
    CFN_PUBLIC_SUBNET = "CFN_PUBLIC_SUBNET"
    '''
    :stability: experimental
    '''
    IAM_ROLE = "IAM_ROLE"
    '''
    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-prototyping-sdk/cdk-graph.EdgeDirectionEnum")
class EdgeDirectionEnum(enum.Enum):
    '''(experimental) EdgeDirection specifies in which direction the edge is directed or if it is undirected.

    :stability: experimental
    '''

    NONE = "NONE"
    '''(experimental) Indicates that edge is *undirected*;

    meaning there is no directional relationship between the **source** and **target**.

    :stability: experimental
    '''
    FORWARD = "FORWARD"
    '''(experimental) Indicates the edge is *directed* from the **source** to the **target**.

    :stability: experimental
    '''
    BACK = "BACK"
    '''(experimental) Indicates the edge is *directed* from the **target** to the **source**.

    :stability: experimental
    '''
    BOTH = "BOTH"
    '''(experimental) Indicates the edge is *bi-directional*.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-prototyping-sdk/cdk-graph.EdgeTypeEnum")
class EdgeTypeEnum(enum.Enum):
    '''(experimental) Edge types handles by the graph.

    :stability: experimental
    '''

    CUSTOM = "CUSTOM"
    '''(experimental) Custom edge.

    :stability: experimental
    '''
    REFERENCE = "REFERENCE"
    '''(experimental) Reference edge (Ref, Fn::GetAtt, Fn::ImportValue).

    :stability: experimental
    '''
    DEPENDENCY = "DEPENDENCY"
    '''(experimental) CloudFormation dependency edge.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-prototyping-sdk/cdk-graph.FilterPreset")
class FilterPreset(enum.Enum):
    '''(experimental) Filter presets.

    :stability: experimental
    '''

    COMPACT = "COMPACT"
    '''(experimental) Collapses extraneous nodes to parent and cdk created nodes on themselves, and prunes extraneous edges.

    This most closely represents the developers code for the current application
    and reduces the noise one expects.

    :stability: experimental
    '''
    NON_EXTRANEOUS = "NON_EXTRANEOUS"
    '''(experimental) Collapses extraneous nodes to parent and prunes extraneous edges.

    :stability: experimental
    '''
    NONE = "NONE"
    '''(experimental) No filtering is performed which will output **verbose** graph.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-prototyping-sdk/cdk-graph.FilterStrategy")
class FilterStrategy(enum.Enum):
    '''(experimental) Filter strategy to apply to filter matches.

    :stability: experimental
    '''

    PRUNE = "PRUNE"
    '''(experimental) Remove filtered entity and all its edges.

    :stability: experimental
    '''
    COLLAPSE = "COLLAPSE"
    '''(experimental) Collapse all child entities of filtered entity into filtered entity;

    and hoist all edges.

    :stability: experimental
    '''
    COLLAPSE_TO_PARENT = "COLLAPSE_TO_PARENT"
    '''(experimental) Collapse all filtered entities into their parent entity;

    and hoist its edges to parent.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-prototyping-sdk/cdk-graph.FlagEnum")
class FlagEnum(enum.Enum):
    '''(experimental) Graph flags.

    :stability: experimental
    '''

    CLUSTER = "CLUSTER"
    '''(experimental) Indicates that node is a cluster (container) and treated like an emphasized subgraph.

    :stability: experimental
    '''
    GRAPH_CONTAINER = "GRAPH_CONTAINER"
    '''(experimental) Indicates that node is non-resource container (Root, App) and used for structural purpose in the graph only.

    :stability: experimental
    '''
    EXTRANEOUS = "EXTRANEOUS"
    '''(experimental) Indicates that the entity is extraneous and considered collapsible to parent without impact of intent.

    :stability: experimental
    '''
    ASSET = "ASSET"
    '''(experimental) Indicates node is considered a CDK Asset (Lambda Code, Docker Image, etc).

    :stability: experimental
    '''
    CDK_OWNED = "CDK_OWNED"
    '''(experimental) Indicates that node was created by CDK.

    :see: https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.Resource.html#static-iswbrownedwbrresourceconstruct
    :stability: experimental
    '''
    CFN_FQN = "CFN_FQN"
    '''(experimental) Indicates node ConstructInfoFqn denotes a ``aws-cdk-lib.*.Cfn*`` construct.

    :stability: experimental
    '''
    CLOSED_EDGE = "CLOSED_EDGE"
    '''(experimental) Indicates that edge is closed;

    meaning ``source === target``. This flag only gets applied on creation of edge, not during mutations to maintain initial intent.

    :stability: experimental
    '''
    MUTATED = "MUTATED"
    '''(experimental) Indicates that entity was mutated;

    meaning a mutation was performed to change originally computed graph value.

    :stability: experimental
    '''
    IMPORT = "IMPORT"
    '''(experimental) Indicates that resource is imported into CDK (eg: ``lambda.Function.fromFunctionName()``, ``s3.Bucket.fromBucketArn()``).

    :stability: experimental
    '''
    CUSTOM_RESOURCE = "CUSTOM_RESOURCE"
    '''(experimental) Indicates if node is a CustomResource.

    :see: https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.custom_resources-readme.html
    :stability: experimental
    '''
    AWS_CUSTOM_RESOURCE = "AWS_CUSTOM_RESOURCE"
    '''(experimental) Indicates if node is an AwsCustomResource, which is a custom resource that simply calls the AWS SDK API via singleton provider.

    :see: https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.custom_resources.AwsCustomResource.html
    :stability: experimental
    '''
    AWS_API_CALL_LAMBDA = "AWS_API_CALL_LAMBDA"
    '''(experimental) Indicates if lambda function resource is a singleton AWS API call lambda for AwsCustomResources.

    :see: https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.custom_resources.AwsCustomResource.html
    :stability: experimental
    '''


@jsii.interface(jsii_type="@aws-prototyping-sdk/cdk-graph.IBaseEntityDataProps")
class IBaseEntityDataProps(typing_extensions.Protocol):
    '''(experimental) Base interface for all store entities **data** props.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="attributes")
    def attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, "PlainObject", typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, "PlainObject"]]]]]:
        '''(experimental) Attributes.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="flags")
    def flags(self) -> typing.Optional[typing.List[FlagEnum]]:
        '''(experimental) Flags.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(
        self,
    ) -> typing.Optional[typing.List[_constructs_77d1e7e8.MetadataEntry]]:
        '''(experimental) Metadata entries.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Tags.

        :stability: experimental
        '''
        ...


class _IBaseEntityDataPropsProxy:
    '''(experimental) Base interface for all store entities **data** props.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph.IBaseEntityDataProps"

    @builtins.property
    @jsii.member(jsii_name="attributes")
    def attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, "PlainObject", typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, "PlainObject"]]]]]:
        '''(experimental) Attributes.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, "PlainObject", typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, "PlainObject"]]]]], jsii.get(self, "attributes"))

    @builtins.property
    @jsii.member(jsii_name="flags")
    def flags(self) -> typing.Optional[typing.List[FlagEnum]]:
        '''(experimental) Flags.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[FlagEnum]], jsii.get(self, "flags"))

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(
        self,
    ) -> typing.Optional[typing.List[_constructs_77d1e7e8.MetadataEntry]]:
        '''(experimental) Metadata entries.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[_constructs_77d1e7e8.MetadataEntry]], jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Tags.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tags"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IBaseEntityDataProps).__jsii_proxy_class__ = lambda : _IBaseEntityDataPropsProxy


@jsii.interface(jsii_type="@aws-prototyping-sdk/cdk-graph.IBaseEntityProps")
class IBaseEntityProps(IBaseEntityDataProps, typing_extensions.Protocol):
    '''(experimental) Base interface for all store entities props.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="store")
    def store(self) -> "Store":
        '''(experimental) Store.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="uuid")
    def uuid(self) -> builtins.str:
        '''(experimental) UUID.

        :stability: experimental
        '''
        ...


class _IBaseEntityPropsProxy(
    jsii.proxy_for(IBaseEntityDataProps), # type: ignore[misc]
):
    '''(experimental) Base interface for all store entities props.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph.IBaseEntityProps"

    @builtins.property
    @jsii.member(jsii_name="store")
    def store(self) -> "Store":
        '''(experimental) Store.

        :stability: experimental
        '''
        return typing.cast("Store", jsii.get(self, "store"))

    @builtins.property
    @jsii.member(jsii_name="uuid")
    def uuid(self) -> builtins.str:
        '''(experimental) UUID.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "uuid"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IBaseEntityProps).__jsii_proxy_class__ = lambda : _IBaseEntityPropsProxy


@jsii.interface(jsii_type="@aws-prototyping-sdk/cdk-graph.ICdkGraphPlugin")
class ICdkGraphPlugin(typing_extensions.Protocol):
    '''(experimental) CdkGraph **Plugin** interface.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''(experimental) Unique identifier for this plugin.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        '''(experimental) Plugin version.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="dependencies")
    def dependencies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of plugins this plugin depends on, including optional semver version (eg: ["foo", "bar@1.2"]).

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="bind")
    def bind(self) -> "IGraphPluginBindCallback":
        '''(experimental) Binds the plugin to the CdkGraph instance.

        Enables plugins to receive base configs.

        :stability: experimental
        '''
        ...

    @bind.setter
    def bind(self, value: "IGraphPluginBindCallback") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="inspect")
    def inspect(self) -> typing.Optional["IGraphVisitorCallback"]:
        '''(experimental) Node visitor callback for construct tree traversal.

        This follows IAspect.visit pattern, but the order
        of visitor traversal in managed by the CdkGraph.

        :stability: experimental
        '''
        ...

    @inspect.setter
    def inspect(self, value: typing.Optional["IGraphVisitorCallback"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="report")
    def report(self) -> typing.Optional["IGraphReportCallback"]:
        '''(experimental) Generate asynchronous reports based on the graph.

        This is not automatically called when synthesizing CDK.
        Developer must explicitly add ``await graphInstance.report()`` to the CDK bin or invoke this outside
        of the CDK synth. In either case, the plugin receives the in-memory graph interface when invoked, as the
        CdkGraph will deserialize the graph prior to invoking the plugin report.

        :stability: experimental
        '''
        ...

    @report.setter
    def report(self, value: typing.Optional["IGraphReportCallback"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="synthesize")
    def synthesize(self) -> typing.Optional["IGraphSynthesizeCallback"]:
        '''(experimental) Called during CDK synthesize to generate synchronous artifacts based on the in-memory graph passed to the plugin.

        This is called in fifo order of plugins.

        :stability: experimental
        '''
        ...

    @synthesize.setter
    def synthesize(self, value: typing.Optional["IGraphSynthesizeCallback"]) -> None:
        ...


class _ICdkGraphPluginProxy:
    '''(experimental) CdkGraph **Plugin** interface.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph.ICdkGraphPlugin"

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''(experimental) Unique identifier for this plugin.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        '''(experimental) Plugin version.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="dependencies")
    def dependencies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of plugins this plugin depends on, including optional semver version (eg: ["foo", "bar@1.2"]).

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dependencies"))

    @builtins.property
    @jsii.member(jsii_name="bind")
    def bind(self) -> "IGraphPluginBindCallback":
        '''(experimental) Binds the plugin to the CdkGraph instance.

        Enables plugins to receive base configs.

        :stability: experimental
        '''
        return typing.cast("IGraphPluginBindCallback", jsii.get(self, "bind"))

    @bind.setter
    def bind(self, value: "IGraphPluginBindCallback") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54a2cc255662b5e0876e8d0db605a73b801eab0609f7115a372a87534496cb3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bind", value)

    @builtins.property
    @jsii.member(jsii_name="inspect")
    def inspect(self) -> typing.Optional["IGraphVisitorCallback"]:
        '''(experimental) Node visitor callback for construct tree traversal.

        This follows IAspect.visit pattern, but the order
        of visitor traversal in managed by the CdkGraph.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["IGraphVisitorCallback"], jsii.get(self, "inspect"))

    @inspect.setter
    def inspect(self, value: typing.Optional["IGraphVisitorCallback"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22f4e280b8570ce4b34179d204a45f016fc59269a033e588b8034098b2fd8a72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inspect", value)

    @builtins.property
    @jsii.member(jsii_name="report")
    def report(self) -> typing.Optional["IGraphReportCallback"]:
        '''(experimental) Generate asynchronous reports based on the graph.

        This is not automatically called when synthesizing CDK.
        Developer must explicitly add ``await graphInstance.report()`` to the CDK bin or invoke this outside
        of the CDK synth. In either case, the plugin receives the in-memory graph interface when invoked, as the
        CdkGraph will deserialize the graph prior to invoking the plugin report.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["IGraphReportCallback"], jsii.get(self, "report"))

    @report.setter
    def report(self, value: typing.Optional["IGraphReportCallback"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc2ff5d90cebb53054076da0d81c370dce67943e3aa06c8a1acd6778dc66ded6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "report", value)

    @builtins.property
    @jsii.member(jsii_name="synthesize")
    def synthesize(self) -> typing.Optional["IGraphSynthesizeCallback"]:
        '''(experimental) Called during CDK synthesize to generate synchronous artifacts based on the in-memory graph passed to the plugin.

        This is called in fifo order of plugins.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["IGraphSynthesizeCallback"], jsii.get(self, "synthesize"))

    @synthesize.setter
    def synthesize(self, value: typing.Optional["IGraphSynthesizeCallback"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f284eaa765a86f8c6ceacf14f7621e610187a734600a8597ddf791545b56252)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "synthesize", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICdkGraphPlugin).__jsii_proxy_class__ = lambda : _ICdkGraphPluginProxy


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/cdk-graph.ICdkGraphProps",
    jsii_struct_bases=[],
    name_mapping={"plugins": "plugins"},
)
class ICdkGraphProps:
    def __init__(
        self,
        *,
        plugins: typing.Optional[typing.Sequence[ICdkGraphPlugin]] = None,
    ) -> None:
        '''(experimental) {@link CdkGraph} props.

        :param plugins: (experimental) List of plugins to extends the graph. Plugins are invoked at each phases in fifo order.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1029a75fabb2077855ce3cf42d58afba32e0ebd9b55995166d157a280e84bc8a)
            check_type(argname="argument plugins", value=plugins, expected_type=type_hints["plugins"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if plugins is not None:
            self._values["plugins"] = plugins

    @builtins.property
    def plugins(self) -> typing.Optional[typing.List[ICdkGraphPlugin]]:
        '''(experimental) List of plugins to extends the graph.

        Plugins are invoked at each phases in fifo order.

        :stability: experimental
        '''
        result = self._values.get("plugins")
        return typing.cast(typing.Optional[typing.List[ICdkGraphPlugin]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ICdkGraphProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-prototyping-sdk/cdk-graph.IEdgePredicate")
class IEdgePredicate(typing_extensions.Protocol):
    '''(experimental) Predicate to match edge.

    :stability: experimental
    '''

    pass


class _IEdgePredicateProxy:
    '''(experimental) Predicate to match edge.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph.IEdgePredicate"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IEdgePredicate).__jsii_proxy_class__ = lambda : _IEdgePredicateProxy


@jsii.interface(jsii_type="@aws-prototyping-sdk/cdk-graph.IFilterFocusCallback")
class IFilterFocusCallback(typing_extensions.Protocol):
    '''(experimental) Determines focus node of filter plan.

    :stability: experimental
    '''

    pass


class _IFilterFocusCallbackProxy:
    '''(experimental) Determines focus node of filter plan.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph.IFilterFocusCallback"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFilterFocusCallback).__jsii_proxy_class__ = lambda : _IFilterFocusCallbackProxy


@jsii.interface(jsii_type="@aws-prototyping-sdk/cdk-graph.IFindEdgeOptions")
class IFindEdgeOptions(typing_extensions.Protocol):
    '''(experimental) Options for edge based search operations.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="order")
    def order(self) -> typing.Optional[_constructs_77d1e7e8.ConstructOrder]:
        '''(experimental) The order of traversal during search path.

        :stability: experimental
        '''
        ...

    @order.setter
    def order(
        self,
        value: typing.Optional[_constructs_77d1e7e8.ConstructOrder],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="predicate")
    def predicate(self) -> typing.Optional[IEdgePredicate]:
        '''(experimental) The predicate to match edges(s).

        :stability: experimental
        '''
        ...

    @predicate.setter
    def predicate(self, value: typing.Optional[IEdgePredicate]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="reverse")
    def reverse(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates reverse order.

        :stability: experimental
        '''
        ...

    @reverse.setter
    def reverse(self, value: typing.Optional[builtins.bool]) -> None:
        ...


class _IFindEdgeOptionsProxy:
    '''(experimental) Options for edge based search operations.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph.IFindEdgeOptions"

    @builtins.property
    @jsii.member(jsii_name="order")
    def order(self) -> typing.Optional[_constructs_77d1e7e8.ConstructOrder]:
        '''(experimental) The order of traversal during search path.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_constructs_77d1e7e8.ConstructOrder], jsii.get(self, "order"))

    @order.setter
    def order(
        self,
        value: typing.Optional[_constructs_77d1e7e8.ConstructOrder],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__440664ecfc99fe6d91fc2446a1d9edaebf3ec63fe4d2dde7ac509deaa8835a48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "order", value)

    @builtins.property
    @jsii.member(jsii_name="predicate")
    def predicate(self) -> typing.Optional[IEdgePredicate]:
        '''(experimental) The predicate to match edges(s).

        :stability: experimental
        '''
        return typing.cast(typing.Optional[IEdgePredicate], jsii.get(self, "predicate"))

    @predicate.setter
    def predicate(self, value: typing.Optional[IEdgePredicate]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c042bf96af1e885eb3a18d82be6e0e70cb7275544df14fe112ecef0343ff731)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "predicate", value)

    @builtins.property
    @jsii.member(jsii_name="reverse")
    def reverse(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates reverse order.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "reverse"))

    @reverse.setter
    def reverse(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ae17a56aa13539018155b42cba0bfdb979e49216bdb763a0858a65e139a8539)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reverse", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFindEdgeOptions).__jsii_proxy_class__ = lambda : _IFindEdgeOptionsProxy


@jsii.interface(jsii_type="@aws-prototyping-sdk/cdk-graph.IFindNodeOptions")
class IFindNodeOptions(typing_extensions.Protocol):
    '''(experimental) Options for node based search operations.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="order")
    def order(self) -> typing.Optional[_constructs_77d1e7e8.ConstructOrder]:
        '''(experimental) The order of traversal during search path.

        :stability: experimental
        '''
        ...

    @order.setter
    def order(
        self,
        value: typing.Optional[_constructs_77d1e7e8.ConstructOrder],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="predicate")
    def predicate(self) -> typing.Optional["INodePredicate"]:
        '''(experimental) The predicate to match node(s).

        :stability: experimental
        '''
        ...

    @predicate.setter
    def predicate(self, value: typing.Optional["INodePredicate"]) -> None:
        ...


class _IFindNodeOptionsProxy:
    '''(experimental) Options for node based search operations.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph.IFindNodeOptions"

    @builtins.property
    @jsii.member(jsii_name="order")
    def order(self) -> typing.Optional[_constructs_77d1e7e8.ConstructOrder]:
        '''(experimental) The order of traversal during search path.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_constructs_77d1e7e8.ConstructOrder], jsii.get(self, "order"))

    @order.setter
    def order(
        self,
        value: typing.Optional[_constructs_77d1e7e8.ConstructOrder],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a17706617442c90e6363c950cb20ba8f09e96181e25fb5918d0dff8c468242e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "order", value)

    @builtins.property
    @jsii.member(jsii_name="predicate")
    def predicate(self) -> typing.Optional["INodePredicate"]:
        '''(experimental) The predicate to match node(s).

        :stability: experimental
        '''
        return typing.cast(typing.Optional["INodePredicate"], jsii.get(self, "predicate"))

    @predicate.setter
    def predicate(self, value: typing.Optional["INodePredicate"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0600443b4cf948de4ef4854854b1f2c81d19ca55dd180c8a00faf7563eeccfa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "predicate", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFindNodeOptions).__jsii_proxy_class__ = lambda : _IFindNodeOptionsProxy


@jsii.interface(jsii_type="@aws-prototyping-sdk/cdk-graph.IGraphFilter")
class IGraphFilter(typing_extensions.Protocol):
    '''(experimental) Graph filter.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="allNodes")
    def all_nodes(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates that all nodes will be filtered, rather than just Resource and CfnResource nodes.

        By enabling this, all Stages, Stacks, and structural construct boundaries will be filtered as well.
        In general, most users intent is to operate against resources and desire to preserve structural groupings,
        which is common in most Cfn/Cdk based filtering where inputs are "include" lists.

        Defaults to value of containing {@link IGraphFilterPlan.allNodes}

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="edge")
    def edge(self) -> typing.Optional[IEdgePredicate]:
        '''(experimental) Predicate to match edges.

        Edges are evaluated after nodes are filtered.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="inverse")
    def inverse(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates that matches will be filtered, as opposed to non-matches.

        The default follows common `Javascript Array.filter <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/filter>`_
        precedence of preserving matches during filtering, while pruning non-matches.

        :default: false - Preserve matches, and filter out non-matches.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="node")
    def node(self) -> typing.Optional["INodePredicate"]:
        '''(experimental) Predicate to match nodes.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def strategy(self) -> typing.Optional[FilterStrategy]:
        '''(experimental) Filter strategy to apply to matching nodes.

        Edges do not have a strategy, they are always pruned.

        :default: {FilterStrategy.PRUNE}

        :stability: experimental
        '''
        ...


class _IGraphFilterProxy:
    '''(experimental) Graph filter.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph.IGraphFilter"

    @builtins.property
    @jsii.member(jsii_name="allNodes")
    def all_nodes(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates that all nodes will be filtered, rather than just Resource and CfnResource nodes.

        By enabling this, all Stages, Stacks, and structural construct boundaries will be filtered as well.
        In general, most users intent is to operate against resources and desire to preserve structural groupings,
        which is common in most Cfn/Cdk based filtering where inputs are "include" lists.

        Defaults to value of containing {@link IGraphFilterPlan.allNodes}

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "allNodes"))

    @builtins.property
    @jsii.member(jsii_name="edge")
    def edge(self) -> typing.Optional[IEdgePredicate]:
        '''(experimental) Predicate to match edges.

        Edges are evaluated after nodes are filtered.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[IEdgePredicate], jsii.get(self, "edge"))

    @builtins.property
    @jsii.member(jsii_name="inverse")
    def inverse(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates that matches will be filtered, as opposed to non-matches.

        The default follows common `Javascript Array.filter <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/filter>`_
        precedence of preserving matches during filtering, while pruning non-matches.

        :default: false - Preserve matches, and filter out non-matches.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "inverse"))

    @builtins.property
    @jsii.member(jsii_name="node")
    def node(self) -> typing.Optional["INodePredicate"]:
        '''(experimental) Predicate to match nodes.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["INodePredicate"], jsii.get(self, "node"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def strategy(self) -> typing.Optional[FilterStrategy]:
        '''(experimental) Filter strategy to apply to matching nodes.

        Edges do not have a strategy, they are always pruned.

        :default: {FilterStrategy.PRUNE}

        :stability: experimental
        '''
        return typing.cast(typing.Optional[FilterStrategy], jsii.get(self, "strategy"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGraphFilter).__jsii_proxy_class__ = lambda : _IGraphFilterProxy


@jsii.interface(jsii_type="@aws-prototyping-sdk/cdk-graph.IGraphFilterPlan")
class IGraphFilterPlan(typing_extensions.Protocol):
    '''(experimental) Graph filter plan.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="allNodes")
    def all_nodes(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates that all nodes will be filtered, rather than just Resource and CfnResource nodes.

        By enabling this, all Stages, Stacks, and structural construct boundaries will be filtered as well.
        In general, most users intent is to operate against resources and desire to preserve structural groupings,
        which is common in most Cfn/Cdk based filtering where inputs are "include" lists.

        :default: false By default only Resource and CfnResource nodes are filtered.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="filters")
    def filters(
        self,
    ) -> typing.Optional[typing.List[typing.Union[IGraphFilter, "IGraphStoreFilter"]]]:
        '''(experimental) Ordered list of {@link IGraphFilter} and {@link IGraphStoreFilter} filters to apply to the store.

        - Filters are applied *after* the preset filtering is applied if present.
        - Filters are applied sequentially against all nodes, as opposed to IAspect.visitor pattern
          which are sequentially applied per node.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="focus")
    def focus(
        self,
    ) -> typing.Optional[typing.Union["Node", IFilterFocusCallback, "IGraphFilterPlanFocusConfig"]]:
        '''(experimental) Config to focus the graph on specific node.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="order")
    def order(self) -> typing.Optional[_constructs_77d1e7e8.ConstructOrder]:
        '''(experimental) The order to visit nodes and edges during filtering.

        :default: {ConstructOrder.PREORDER}

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="preset")
    def preset(self) -> typing.Optional[FilterPreset]:
        '''(experimental) Optional preset filter to apply before other filters.

        :stability: experimental
        '''
        ...


class _IGraphFilterPlanProxy:
    '''(experimental) Graph filter plan.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph.IGraphFilterPlan"

    @builtins.property
    @jsii.member(jsii_name="allNodes")
    def all_nodes(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates that all nodes will be filtered, rather than just Resource and CfnResource nodes.

        By enabling this, all Stages, Stacks, and structural construct boundaries will be filtered as well.
        In general, most users intent is to operate against resources and desire to preserve structural groupings,
        which is common in most Cfn/Cdk based filtering where inputs are "include" lists.

        :default: false By default only Resource and CfnResource nodes are filtered.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "allNodes"))

    @builtins.property
    @jsii.member(jsii_name="filters")
    def filters(
        self,
    ) -> typing.Optional[typing.List[typing.Union[IGraphFilter, "IGraphStoreFilter"]]]:
        '''(experimental) Ordered list of {@link IGraphFilter} and {@link IGraphStoreFilter} filters to apply to the store.

        - Filters are applied *after* the preset filtering is applied if present.
        - Filters are applied sequentially against all nodes, as opposed to IAspect.visitor pattern
          which are sequentially applied per node.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[typing.Union[IGraphFilter, "IGraphStoreFilter"]]], jsii.get(self, "filters"))

    @builtins.property
    @jsii.member(jsii_name="focus")
    def focus(
        self,
    ) -> typing.Optional[typing.Union["Node", IFilterFocusCallback, "IGraphFilterPlanFocusConfig"]]:
        '''(experimental) Config to focus the graph on specific node.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union["Node", IFilterFocusCallback, "IGraphFilterPlanFocusConfig"]], jsii.get(self, "focus"))

    @builtins.property
    @jsii.member(jsii_name="order")
    def order(self) -> typing.Optional[_constructs_77d1e7e8.ConstructOrder]:
        '''(experimental) The order to visit nodes and edges during filtering.

        :default: {ConstructOrder.PREORDER}

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_constructs_77d1e7e8.ConstructOrder], jsii.get(self, "order"))

    @builtins.property
    @jsii.member(jsii_name="preset")
    def preset(self) -> typing.Optional[FilterPreset]:
        '''(experimental) Optional preset filter to apply before other filters.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[FilterPreset], jsii.get(self, "preset"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGraphFilterPlan).__jsii_proxy_class__ = lambda : _IGraphFilterPlanProxy


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/cdk-graph.IGraphFilterPlanFocusConfig",
    jsii_struct_bases=[],
    name_mapping={"node": "node", "no_hoist": "noHoist"},
)
class IGraphFilterPlanFocusConfig:
    def __init__(
        self,
        *,
        node: typing.Union["Node", IFilterFocusCallback],
        no_hoist: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param node: (experimental) The node or resolver to determine the node to focus on.
        :param no_hoist: (experimental) Indicates if ancestral containers are preserved (eg: Stages, Stack). If ``false``, the "focused node" will be hoisted to the graph root and all ancestors will be pruned. If ``true``, the "focused" will be left in-place, while all siblings and non-scope ancestors will be pruned. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6241e99a37312065c459cc9683e037e64c397e027b88a5b903d7cbabb1ac8ea)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
            check_type(argname="argument no_hoist", value=no_hoist, expected_type=type_hints["no_hoist"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "node": node,
        }
        if no_hoist is not None:
            self._values["no_hoist"] = no_hoist

    @builtins.property
    def node(self) -> typing.Union["Node", IFilterFocusCallback]:
        '''(experimental) The node or resolver to determine the node to focus on.

        :stability: experimental
        '''
        result = self._values.get("node")
        assert result is not None, "Required property 'node' is missing"
        return typing.cast(typing.Union["Node", IFilterFocusCallback], result)

    @builtins.property
    def no_hoist(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates if ancestral containers are preserved (eg: Stages, Stack).

        If ``false``, the "focused node" will be hoisted to the graph root and all ancestors will be pruned.
        If ``true``, the "focused" will be left in-place, while all siblings and non-scope ancestors will be pruned.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("no_hoist")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IGraphFilterPlanFocusConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-prototyping-sdk/cdk-graph.IGraphPluginBindCallback")
class IGraphPluginBindCallback(typing_extensions.Protocol):
    '''(experimental) Callback signature for graph ``Plugin.bind`` operation.

    :stability: experimental
    '''

    pass


class _IGraphPluginBindCallbackProxy:
    '''(experimental) Callback signature for graph ``Plugin.bind`` operation.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph.IGraphPluginBindCallback"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGraphPluginBindCallback).__jsii_proxy_class__ = lambda : _IGraphPluginBindCallbackProxy


@jsii.interface(jsii_type="@aws-prototyping-sdk/cdk-graph.IGraphReportCallback")
class IGraphReportCallback(typing_extensions.Protocol):
    '''(experimental) Callback signature for graph ``Plugin.report`` operation.

    :stability: experimental
    '''

    pass


class _IGraphReportCallbackProxy:
    '''(experimental) Callback signature for graph ``Plugin.report`` operation.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph.IGraphReportCallback"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGraphReportCallback).__jsii_proxy_class__ = lambda : _IGraphReportCallbackProxy


@jsii.interface(jsii_type="@aws-prototyping-sdk/cdk-graph.IGraphStoreFilter")
class IGraphStoreFilter(typing_extensions.Protocol):
    '''(experimental) Store filter callback interface used to perform filtering operations directly against the store, as opposed to using {@link IGraphFilter} definitions.

    :stability: experimental
    '''

    pass


class _IGraphStoreFilterProxy:
    '''(experimental) Store filter callback interface used to perform filtering operations directly against the store, as opposed to using {@link IGraphFilter} definitions.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph.IGraphStoreFilter"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGraphStoreFilter).__jsii_proxy_class__ = lambda : _IGraphStoreFilterProxy


@jsii.interface(jsii_type="@aws-prototyping-sdk/cdk-graph.IGraphSynthesizeCallback")
class IGraphSynthesizeCallback(typing_extensions.Protocol):
    '''(experimental) Callback signature for graph ``Plugin.synthesize`` operation.

    :stability: experimental
    '''

    pass


class _IGraphSynthesizeCallbackProxy:
    '''(experimental) Callback signature for graph ``Plugin.synthesize`` operation.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph.IGraphSynthesizeCallback"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGraphSynthesizeCallback).__jsii_proxy_class__ = lambda : _IGraphSynthesizeCallbackProxy


@jsii.interface(jsii_type="@aws-prototyping-sdk/cdk-graph.IGraphVisitorCallback")
class IGraphVisitorCallback(typing_extensions.Protocol):
    '''(experimental) Callback signature for graph ``Plugin.inspect`` operation.

    :stability: experimental
    '''

    pass


class _IGraphVisitorCallbackProxy:
    '''(experimental) Callback signature for graph ``Plugin.inspect`` operation.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph.IGraphVisitorCallback"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGraphVisitorCallback).__jsii_proxy_class__ = lambda : _IGraphVisitorCallbackProxy


@jsii.interface(jsii_type="@aws-prototyping-sdk/cdk-graph.INodePredicate")
class INodePredicate(typing_extensions.Protocol):
    '''(experimental) Predicate to match node.

    :stability: experimental
    '''

    pass


class _INodePredicateProxy:
    '''(experimental) Predicate to match node.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph.INodePredicate"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INodePredicate).__jsii_proxy_class__ = lambda : _INodePredicateProxy


@jsii.interface(jsii_type="@aws-prototyping-sdk/cdk-graph.ISerializableEdge")
class ISerializableEdge(typing_extensions.Protocol):
    '''(experimental) Interface for serializable graph edge entity.

    :stability: experimental
    '''

    pass


class _ISerializableEdgeProxy:
    '''(experimental) Interface for serializable graph edge entity.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph.ISerializableEdge"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISerializableEdge).__jsii_proxy_class__ = lambda : _ISerializableEdgeProxy


@jsii.interface(jsii_type="@aws-prototyping-sdk/cdk-graph.ISerializableEntity")
class ISerializableEntity(typing_extensions.Protocol):
    '''(experimental) Interface for serializable graph entities.

    :stability: experimental
    '''

    pass


class _ISerializableEntityProxy:
    '''(experimental) Interface for serializable graph entities.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph.ISerializableEntity"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISerializableEntity).__jsii_proxy_class__ = lambda : _ISerializableEntityProxy


@jsii.interface(jsii_type="@aws-prototyping-sdk/cdk-graph.ISerializableGraphStore")
class ISerializableGraphStore(typing_extensions.Protocol):
    '''(experimental) Interface for serializable graph store.

    :stability: experimental
    '''

    @jsii.member(jsii_name="serialize")
    def serialize(self) -> "SGGraphStore":
        '''
        :stability: experimental
        '''
        ...


class _ISerializableGraphStoreProxy:
    '''(experimental) Interface for serializable graph store.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph.ISerializableGraphStore"

    @jsii.member(jsii_name="serialize")
    def serialize(self) -> "SGGraphStore":
        '''
        :stability: experimental
        '''
        return typing.cast("SGGraphStore", jsii.invoke(self, "serialize", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISerializableGraphStore).__jsii_proxy_class__ = lambda : _ISerializableGraphStoreProxy


@jsii.interface(jsii_type="@aws-prototyping-sdk/cdk-graph.ISerializableNode")
class ISerializableNode(typing_extensions.Protocol):
    '''(experimental) Interface for serializable graph node entity.

    :stability: experimental
    '''

    pass


class _ISerializableNodeProxy:
    '''(experimental) Interface for serializable graph node entity.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph.ISerializableNode"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISerializableNode).__jsii_proxy_class__ = lambda : _ISerializableNodeProxy


@jsii.interface(jsii_type="@aws-prototyping-sdk/cdk-graph.IStoreCounts")
class IStoreCounts(typing_extensions.Protocol):
    '''(experimental) Interface for store counts.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="cfnResources")
    def cfn_resources(self) -> typing.Mapping[builtins.str, jsii.Number]:
        '''(experimental) Returns {@link ICounterRecord} containing total number of each *cfnResourceType*.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="edges")
    def edges(self) -> jsii.Number:
        '''(experimental) Counts total number of edges in the store.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="edgeTypes")
    def edge_types(self) -> typing.Mapping[builtins.str, jsii.Number]:
        '''(experimental) Returns {@link ICounterRecord} containing total number of each *edge type* ({@link EdgeTypeEnum}).

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="nodes")
    def nodes(self) -> jsii.Number:
        '''(experimental) Counts total number of nodes in the store.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="nodeTypes")
    def node_types(self) -> typing.Mapping[builtins.str, jsii.Number]:
        '''(experimental) Returns {@link ICounterRecord} containing total number of each *node type* ({@link NodeTypeEnum}).

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> jsii.Number:
        '''(experimental) Counts total number of stacks in the store.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="stages")
    def stages(self) -> jsii.Number:
        '''(experimental) Counts total number of stages in the store.

        :stability: experimental
        '''
        ...


class _IStoreCountsProxy:
    '''(experimental) Interface for store counts.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph.IStoreCounts"

    @builtins.property
    @jsii.member(jsii_name="cfnResources")
    def cfn_resources(self) -> typing.Mapping[builtins.str, jsii.Number]:
        '''(experimental) Returns {@link ICounterRecord} containing total number of each *cfnResourceType*.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, jsii.Number], jsii.get(self, "cfnResources"))

    @builtins.property
    @jsii.member(jsii_name="edges")
    def edges(self) -> jsii.Number:
        '''(experimental) Counts total number of edges in the store.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "edges"))

    @builtins.property
    @jsii.member(jsii_name="edgeTypes")
    def edge_types(self) -> typing.Mapping[builtins.str, jsii.Number]:
        '''(experimental) Returns {@link ICounterRecord} containing total number of each *edge type* ({@link EdgeTypeEnum}).

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, jsii.Number], jsii.get(self, "edgeTypes"))

    @builtins.property
    @jsii.member(jsii_name="nodes")
    def nodes(self) -> jsii.Number:
        '''(experimental) Counts total number of nodes in the store.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "nodes"))

    @builtins.property
    @jsii.member(jsii_name="nodeTypes")
    def node_types(self) -> typing.Mapping[builtins.str, jsii.Number]:
        '''(experimental) Returns {@link ICounterRecord} containing total number of each *node type* ({@link NodeTypeEnum}).

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, jsii.Number], jsii.get(self, "nodeTypes"))

    @builtins.property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> jsii.Number:
        '''(experimental) Counts total number of stacks in the store.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "stacks"))

    @builtins.property
    @jsii.member(jsii_name="stages")
    def stages(self) -> jsii.Number:
        '''(experimental) Counts total number of stages in the store.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "stages"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IStoreCounts).__jsii_proxy_class__ = lambda : _IStoreCountsProxy


@jsii.interface(jsii_type="@aws-prototyping-sdk/cdk-graph.ITypedEdgeProps")
class ITypedEdgeProps(IBaseEntityProps, typing_extensions.Protocol):
    '''(experimental) Base edge props agnostic to edge type.

    Used for extending per edge class with type specifics.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> "Node":
        '''(experimental) Edge **source** is the node that defines the edge (tail).

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "Node":
        '''(experimental) Edge **target** is the node being referenced by the **source** (head).

        :stability: experimental
        '''
        ...


class _ITypedEdgePropsProxy(
    jsii.proxy_for(IBaseEntityProps), # type: ignore[misc]
):
    '''(experimental) Base edge props agnostic to edge type.

    Used for extending per edge class with type specifics.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph.ITypedEdgeProps"

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> "Node":
        '''(experimental) Edge **source** is the node that defines the edge (tail).

        :stability: experimental
        '''
        return typing.cast("Node", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "Node":
        '''(experimental) Edge **target** is the node being referenced by the **source** (head).

        :stability: experimental
        '''
        return typing.cast("Node", jsii.get(self, "target"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITypedEdgeProps).__jsii_proxy_class__ = lambda : _ITypedEdgePropsProxy


@jsii.interface(jsii_type="@aws-prototyping-sdk/cdk-graph.ITypedNodeProps")
class ITypedNodeProps(IBaseEntityProps, typing_extensions.Protocol):
    '''(experimental) Base node props agnostic to node type.

    Used for extending per node class with type specifics.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''(experimental) Node id, which is unique within parent scope.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        '''(experimental) Path of the node.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="cfnType")
    def cfn_type(self) -> typing.Optional[builtins.str]:
        '''(experimental) Type of CloudFormation resource.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="constructInfo")
    def construct_info(self) -> typing.Optional[ConstructInfo]:
        '''(experimental) Synthesized construct information defining jii resolution data.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="logicalId")
    def logical_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) Logical id of the node, which is only unique within containing stack.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> typing.Optional["Node"]:
        '''(experimental) Parent node.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> typing.Optional["StackNode"]:
        '''(experimental) Stack the node is contained.

        :stability: experimental
        '''
        ...


class _ITypedNodePropsProxy(
    jsii.proxy_for(IBaseEntityProps), # type: ignore[misc]
):
    '''(experimental) Base node props agnostic to node type.

    Used for extending per node class with type specifics.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph.ITypedNodeProps"

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''(experimental) Node id, which is unique within parent scope.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        '''(experimental) Path of the node.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="cfnType")
    def cfn_type(self) -> typing.Optional[builtins.str]:
        '''(experimental) Type of CloudFormation resource.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cfnType"))

    @builtins.property
    @jsii.member(jsii_name="constructInfo")
    def construct_info(self) -> typing.Optional[ConstructInfo]:
        '''(experimental) Synthesized construct information defining jii resolution data.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[ConstructInfo], jsii.get(self, "constructInfo"))

    @builtins.property
    @jsii.member(jsii_name="logicalId")
    def logical_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) Logical id of the node, which is only unique within containing stack.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logicalId"))

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> typing.Optional["Node"]:
        '''(experimental) Parent node.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["Node"], jsii.get(self, "parent"))

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> typing.Optional["StackNode"]:
        '''(experimental) Stack the node is contained.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["StackNode"], jsii.get(self, "stack"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITypedNodeProps).__jsii_proxy_class__ = lambda : _ITypedNodePropsProxy


@jsii.enum(jsii_type="@aws-prototyping-sdk/cdk-graph.MetadataTypeEnum")
class MetadataTypeEnum(enum.Enum):
    '''(experimental) Common cdk metadata types.

    :stability: experimental
    '''

    LOGICAL_ID = "LOGICAL_ID"
    '''
    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-prototyping-sdk/cdk-graph.NodeTypeEnum")
class NodeTypeEnum(enum.Enum):
    '''(experimental) Node types handled by the graph.

    :stability: experimental
    '''

    DEFAULT = "DEFAULT"
    '''(experimental) Default node type - used for all nodes that don't have explicit type defined.

    :stability: experimental
    '''
    CFN_RESOURCE = "CFN_RESOURCE"
    '''(experimental) L1 cfn resource node.

    :stability: experimental
    '''
    RESOURCE = "RESOURCE"
    '''(experimental) L2 cdk resource node.

    :stability: experimental
    '''
    CUSTOM_RESOURCE = "CUSTOM_RESOURCE"
    '''(experimental) Cdk customer resource node.

    :stability: experimental
    '''
    ROOT = "ROOT"
    '''(experimental) Graph root node.

    :stability: experimental
    '''
    APP = "APP"
    '''(experimental) Cdk App node.

    :stability: experimental
    '''
    STAGE = "STAGE"
    '''(experimental) Cdk Stage node.

    :stability: experimental
    '''
    STACK = "STACK"
    '''(experimental) Cdk Stack node.

    :stability: experimental
    '''
    NESTED_STACK = "NESTED_STACK"
    '''(experimental) Cdk NestedStack node.

    :stability: experimental
    '''
    OUTPUT = "OUTPUT"
    '''(experimental) CfnOutput node.

    :stability: experimental
    '''
    PARAMETER = "PARAMETER"
    '''(experimental) CfnParameter node.

    :stability: experimental
    '''
    ASSET = "ASSET"
    '''(experimental) Cdk asset node.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/cdk-graph.PlainObject",
    jsii_struct_bases=[],
    name_mapping={},
)
class PlainObject:
    def __init__(self) -> None:
        '''(experimental) Serializable plain object value (JSII supported).

        :stability: experimental
        '''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PlainObject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-prototyping-sdk/cdk-graph.ReferenceTypeEnum")
class ReferenceTypeEnum(enum.Enum):
    '''(experimental) Reference edge types.

    :stability: experimental
    '''

    REF = "REF"
    '''(experimental) CloudFormation **Ref** reference.

    :stability: experimental
    '''
    ATTRIBUTE = "ATTRIBUTE"
    '''(experimental) CloudFormation **Fn::GetAtt** reference.

    :stability: experimental
    '''
    IMPORT = "IMPORT"
    '''(experimental) CloudFormation **Fn::ImportValue** reference.

    :stability: experimental
    '''
    IMPORT_ARN = "IMPORT_ARN"
    '''(experimental) CloudFormation **Fn::Join** reference of imported resourced (eg: ``s3.Bucket.fromBucketArn()``).

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/cdk-graph.SGEntity",
    jsii_struct_bases=[],
    name_mapping={
        "uuid": "uuid",
        "attributes": "attributes",
        "flags": "flags",
        "metadata": "metadata",
        "tags": "tags",
    },
)
class SGEntity:
    def __init__(
        self,
        *,
        uuid: builtins.str,
        attributes: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]]]]]]] = None,
        flags: typing.Optional[typing.Sequence[FlagEnum]] = None,
        metadata: typing.Optional[typing.Sequence[typing.Union[_constructs_77d1e7e8.MetadataEntry, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''(experimental) Serializable graph entity.

        :param uuid: (experimental) Universally unique identity.
        :param attributes: (experimental) Serializable entity attributes.
        :param flags: (experimental) Serializable entity flags.
        :param metadata: (experimental) Serializable entity metadata.
        :param tags: (experimental) Serializable entity tags.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc362a68986d00030e674b435fe815be827570aa7f8a93400db488245da5a627)
            check_type(argname="argument uuid", value=uuid, expected_type=type_hints["uuid"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument flags", value=flags, expected_type=type_hints["flags"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uuid": uuid,
        }
        if attributes is not None:
            self._values["attributes"] = attributes
        if flags is not None:
            self._values["flags"] = flags
        if metadata is not None:
            self._values["metadata"] = metadata
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def uuid(self) -> builtins.str:
        '''(experimental) Universally unique identity.

        :stability: experimental
        '''
        result = self._values.get("uuid")
        assert result is not None, "Required property 'uuid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]]]:
        '''(experimental) Serializable entity attributes.

        :see: {@link Attributes }
        :stability: experimental
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]]], result)

    @builtins.property
    def flags(self) -> typing.Optional[typing.List[FlagEnum]]:
        '''(experimental) Serializable entity flags.

        :see: {@link FlagEnum }
        :stability: experimental
        '''
        result = self._values.get("flags")
        return typing.cast(typing.Optional[typing.List[FlagEnum]], result)

    @builtins.property
    def metadata(
        self,
    ) -> typing.Optional[typing.List[_constructs_77d1e7e8.MetadataEntry]]:
        '''(experimental) Serializable entity metadata.

        :see: {@link Metadata }
        :stability: experimental
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.List[_constructs_77d1e7e8.MetadataEntry]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Serializable entity tags.

        :see: {@link Tags }
        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SGEntity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/cdk-graph.SGGraphStore",
    jsii_struct_bases=[],
    name_mapping={"edges": "edges", "tree": "tree", "version": "version"},
)
class SGGraphStore:
    def __init__(
        self,
        *,
        edges: typing.Sequence[typing.Union["SGEdge", typing.Dict[builtins.str, typing.Any]]],
        tree: typing.Union["SGNode", typing.Dict[builtins.str, typing.Any]],
        version: builtins.str,
    ) -> None:
        '''(experimental) Serializable graph store.

        :param edges: (experimental) List of edges.
        :param tree: (experimental) Node tree.
        :param version: (experimental) Store version.

        :stability: experimental
        '''
        if isinstance(tree, dict):
            tree = SGNode(**tree)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf966f76b2c4db416b9d33d4b216fd881dc8b2fade8b9cf53ee5938a99e87b45)
            check_type(argname="argument edges", value=edges, expected_type=type_hints["edges"])
            check_type(argname="argument tree", value=tree, expected_type=type_hints["tree"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "edges": edges,
            "tree": tree,
            "version": version,
        }

    @builtins.property
    def edges(self) -> typing.List["SGEdge"]:
        '''(experimental) List of edges.

        :stability: experimental
        '''
        result = self._values.get("edges")
        assert result is not None, "Required property 'edges' is missing"
        return typing.cast(typing.List["SGEdge"], result)

    @builtins.property
    def tree(self) -> "SGNode":
        '''(experimental) Node tree.

        :stability: experimental
        '''
        result = self._values.get("tree")
        assert result is not None, "Required property 'tree' is missing"
        return typing.cast("SGNode", result)

    @builtins.property
    def version(self) -> builtins.str:
        '''(experimental) Store version.

        :stability: experimental
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SGGraphStore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/cdk-graph.SGNode",
    jsii_struct_bases=[SGEntity],
    name_mapping={
        "uuid": "uuid",
        "attributes": "attributes",
        "flags": "flags",
        "metadata": "metadata",
        "tags": "tags",
        "id": "id",
        "node_type": "nodeType",
        "path": "path",
        "cfn_type": "cfnType",
        "children": "children",
        "construct_info": "constructInfo",
        "edges": "edges",
        "logical_id": "logicalId",
        "parent": "parent",
        "stack": "stack",
    },
)
class SGNode(SGEntity):
    def __init__(
        self,
        *,
        uuid: builtins.str,
        attributes: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]]]]]]] = None,
        flags: typing.Optional[typing.Sequence[FlagEnum]] = None,
        metadata: typing.Optional[typing.Sequence[typing.Union[_constructs_77d1e7e8.MetadataEntry, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        id: builtins.str,
        node_type: NodeTypeEnum,
        path: builtins.str,
        cfn_type: typing.Optional[builtins.str] = None,
        children: typing.Optional[typing.Mapping[builtins.str, typing.Union["SGNode", typing.Dict[builtins.str, typing.Any]]]] = None,
        construct_info: typing.Optional[typing.Union[ConstructInfo, typing.Dict[builtins.str, typing.Any]]] = None,
        edges: typing.Optional[typing.Sequence[builtins.str]] = None,
        logical_id: typing.Optional[builtins.str] = None,
        parent: typing.Optional[builtins.str] = None,
        stack: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Serializable graph node entity.

        :param uuid: (experimental) Universally unique identity.
        :param attributes: (experimental) Serializable entity attributes.
        :param flags: (experimental) Serializable entity flags.
        :param metadata: (experimental) Serializable entity metadata.
        :param tags: (experimental) Serializable entity tags.
        :param id: (experimental) Node id within parent (unique only between parent child nodes).
        :param node_type: (experimental) Node type.
        :param path: (experimental) Node path.
        :param cfn_type: (experimental) CloudFormation resource type for this node.
        :param children: (experimental) Child node record.
        :param construct_info: (experimental) Synthesized construct information defining jii resolution data.
        :param edges: (experimental) List of edge UUIDs where this node is the **source**.
        :param logical_id: (experimental) Logical id of the node, which is only unique within containing stack.
        :param parent: (experimental) UUID of node parent.
        :param stack: (experimental) UUID of node stack.

        :stability: experimental
        '''
        if isinstance(construct_info, dict):
            construct_info = ConstructInfo(**construct_info)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1f023a3fe8a734d710d6155e34fc386bdcd7777295273f810fb4335bf7750f3)
            check_type(argname="argument uuid", value=uuid, expected_type=type_hints["uuid"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument flags", value=flags, expected_type=type_hints["flags"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument node_type", value=node_type, expected_type=type_hints["node_type"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument cfn_type", value=cfn_type, expected_type=type_hints["cfn_type"])
            check_type(argname="argument children", value=children, expected_type=type_hints["children"])
            check_type(argname="argument construct_info", value=construct_info, expected_type=type_hints["construct_info"])
            check_type(argname="argument edges", value=edges, expected_type=type_hints["edges"])
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uuid": uuid,
            "id": id,
            "node_type": node_type,
            "path": path,
        }
        if attributes is not None:
            self._values["attributes"] = attributes
        if flags is not None:
            self._values["flags"] = flags
        if metadata is not None:
            self._values["metadata"] = metadata
        if tags is not None:
            self._values["tags"] = tags
        if cfn_type is not None:
            self._values["cfn_type"] = cfn_type
        if children is not None:
            self._values["children"] = children
        if construct_info is not None:
            self._values["construct_info"] = construct_info
        if edges is not None:
            self._values["edges"] = edges
        if logical_id is not None:
            self._values["logical_id"] = logical_id
        if parent is not None:
            self._values["parent"] = parent
        if stack is not None:
            self._values["stack"] = stack

    @builtins.property
    def uuid(self) -> builtins.str:
        '''(experimental) Universally unique identity.

        :stability: experimental
        '''
        result = self._values.get("uuid")
        assert result is not None, "Required property 'uuid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]]]:
        '''(experimental) Serializable entity attributes.

        :see: {@link Attributes }
        :stability: experimental
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]]], result)

    @builtins.property
    def flags(self) -> typing.Optional[typing.List[FlagEnum]]:
        '''(experimental) Serializable entity flags.

        :see: {@link FlagEnum }
        :stability: experimental
        '''
        result = self._values.get("flags")
        return typing.cast(typing.Optional[typing.List[FlagEnum]], result)

    @builtins.property
    def metadata(
        self,
    ) -> typing.Optional[typing.List[_constructs_77d1e7e8.MetadataEntry]]:
        '''(experimental) Serializable entity metadata.

        :see: {@link Metadata }
        :stability: experimental
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.List[_constructs_77d1e7e8.MetadataEntry]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Serializable entity tags.

        :see: {@link Tags }
        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def id(self) -> builtins.str:
        '''(experimental) Node id within parent (unique only between parent child nodes).

        :stability: experimental
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def node_type(self) -> NodeTypeEnum:
        '''(experimental) Node type.

        :stability: experimental
        '''
        result = self._values.get("node_type")
        assert result is not None, "Required property 'node_type' is missing"
        return typing.cast(NodeTypeEnum, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''(experimental) Node path.

        :stability: experimental
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cfn_type(self) -> typing.Optional[builtins.str]:
        '''(experimental) CloudFormation resource type for this node.

        :stability: experimental
        '''
        result = self._values.get("cfn_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def children(self) -> typing.Optional[typing.Mapping[builtins.str, "SGNode"]]:
        '''(experimental) Child node record.

        :stability: experimental
        '''
        result = self._values.get("children")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "SGNode"]], result)

    @builtins.property
    def construct_info(self) -> typing.Optional[ConstructInfo]:
        '''(experimental) Synthesized construct information defining jii resolution data.

        :stability: experimental
        '''
        result = self._values.get("construct_info")
        return typing.cast(typing.Optional[ConstructInfo], result)

    @builtins.property
    def edges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of edge UUIDs where this node is the **source**.

        :stability: experimental
        '''
        result = self._values.get("edges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def logical_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) Logical id of the node, which is only unique within containing stack.

        :stability: experimental
        '''
        result = self._values.get("logical_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent(self) -> typing.Optional[builtins.str]:
        '''(experimental) UUID of node parent.

        :stability: experimental
        '''
        result = self._values.get("parent")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stack(self) -> typing.Optional[builtins.str]:
        '''(experimental) UUID of node stack.

        :stability: experimental
        '''
        result = self._values.get("stack")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SGNode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/cdk-graph.SGUnresolvedReference",
    jsii_struct_bases=[],
    name_mapping={
        "reference_type": "referenceType",
        "source": "source",
        "target": "target",
        "value": "value",
    },
)
class SGUnresolvedReference:
    def __init__(
        self,
        *,
        reference_type: ReferenceTypeEnum,
        source: builtins.str,
        target: builtins.str,
        value: typing.Optional[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''(experimental) Unresolved reference struct.

        During graph computation references are unresolved and stored in this struct.

        :param reference_type: 
        :param source: 
        :param target: 
        :param value: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__093efbca62496222f83dc4c926674b4af60ecc878556c3dc198dc6a5a6e2fc8f)
            check_type(argname="argument reference_type", value=reference_type, expected_type=type_hints["reference_type"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "reference_type": reference_type,
            "source": source,
            "target": target,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def reference_type(self) -> ReferenceTypeEnum:
        '''
        :stability: experimental
        '''
        result = self._values.get("reference_type")
        assert result is not None, "Required property 'reference_type' is missing"
        return typing.cast(ReferenceTypeEnum, result)

    @builtins.property
    def source(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SGUnresolvedReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ISerializableGraphStore)
class Store(metaclass=jsii.JSIIMeta, jsii_type="@aws-prototyping-sdk/cdk-graph.Store"):
    '''(experimental) Store class provides the in-memory database-like interface for managing all entities in the graph.

    :stability: experimental
    '''

    def __init__(
        self,
        allow_destructive_mutations: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param allow_destructive_mutations: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c0791921f25556bbc2c8164d44d2289761731e68c2598a9cba96f175f256a73)
            check_type(argname="argument allow_destructive_mutations", value=allow_destructive_mutations, expected_type=type_hints["allow_destructive_mutations"])
        jsii.create(self.__class__, self, [allow_destructive_mutations])

    @jsii.member(jsii_name="fromSerializedStore")
    @builtins.classmethod
    def from_serialized_store(
        cls,
        *,
        edges: typing.Sequence[typing.Union["SGEdge", typing.Dict[builtins.str, typing.Any]]],
        tree: typing.Union[SGNode, typing.Dict[builtins.str, typing.Any]],
        version: builtins.str,
    ) -> "Store":
        '''(experimental) Builds store from serialized store data.

        :param edges: (experimental) List of edges.
        :param tree: (experimental) Node tree.
        :param version: (experimental) Store version.

        :stability: experimental
        '''
        serialized_store = SGGraphStore(edges=edges, tree=tree, version=version)

        return typing.cast("Store", jsii.sinvoke(cls, "fromSerializedStore", [serialized_store]))

    @jsii.member(jsii_name="addEdge")
    def add_edge(self, edge: "Edge") -> None:
        '''(experimental) Add **edge** to the store.

        :param edge: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ded7d912211e7b50ae46a74ae7bf9b68ce262a10ed352fa6b3eb9553a668baa)
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
        return typing.cast(None, jsii.invoke(self, "addEdge", [edge]))

    @jsii.member(jsii_name="addNode")
    def add_node(self, node: "Node") -> None:
        '''(experimental) Add **node** to the store.

        :param node: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbaabc9ec5dfc8d77fe2479d07f0f1c17e60a13e8d6f57804dbb9d93d470ad39)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "addNode", [node]))

    @jsii.member(jsii_name="addStack")
    def add_stack(self, stack: "StackNode") -> None:
        '''(experimental) Add **stack** node to the store.

        :param stack: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15c6a25d652e9961baf37dad48966d941983042cd9bbdd23a6f07ee97e4976a5)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        return typing.cast(None, jsii.invoke(self, "addStack", [stack]))

    @jsii.member(jsii_name="addStage")
    def add_stage(self, stage: "StageNode") -> None:
        '''(experimental) Add **stage** to the store.

        :param stage: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e65b41882a8ab0b9d784a00e3fc56d3701a36386ebb7cfea42f2aeeb5ec1e836)
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        return typing.cast(None, jsii.invoke(self, "addStage", [stage]))

    @jsii.member(jsii_name="clone")
    def clone(
        self,
        allow_destructive_mutations: typing.Optional[builtins.bool] = None,
    ) -> "Store":
        '''(experimental) Clone the store to allow destructive mutations.

        :param allow_destructive_mutations: Indicates if destructive mutations are allowed; defaults to ``true``

        :return: Returns a clone of the store that allows destructive mutations

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebc9b96e7664c6e4ab1e6760d98dd03bcb42b46f6eed7a831092a894c072aa7c)
            check_type(argname="argument allow_destructive_mutations", value=allow_destructive_mutations, expected_type=type_hints["allow_destructive_mutations"])
        return typing.cast("Store", jsii.invoke(self, "clone", [allow_destructive_mutations]))

    @jsii.member(jsii_name="computeLogicalUniversalId")
    def compute_logical_universal_id(
        self,
        stack: "StackNode",
        logical_id: builtins.str,
    ) -> builtins.str:
        '''(experimental) Compute **universal** *logicalId* based on parent stack and construct *logicalId* (``<stack>:<logicalId>``).

        Construct *logicalIds are only unique within their containing stack, so to use *logicalId*
        lookups universally (like resolving references) we need a universal key.

        :param stack: -
        :param logical_id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79fd3c45504b00281faf400a4966b73587a2e09d9ae05c73a23eaae2d6a1e670)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
        return typing.cast(builtins.str, jsii.invoke(self, "computeLogicalUniversalId", [stack, logical_id]))

    @jsii.member(jsii_name="findNodeByImportArn")
    def find_node_by_import_arn(self, value: typing.Any) -> typing.Optional["Node"]:
        '''(experimental) Attempts to lookup the {@link Node} associated with a given *import arn token*.

        :param value: Import arn value, which is either object to tokenize or already tokenized string.

        :return: Returns matching {@link Node } if found, otherwise undefined.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee6be88664b09024a938ab1084f8eaf5be8582aff6546f7694717d08183a4001)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(typing.Optional["Node"], jsii.invoke(self, "findNodeByImportArn", [value]))

    @jsii.member(jsii_name="findNodeByLogicalId")
    def find_node_by_logical_id(
        self,
        stack: "StackNode",
        logical_id: builtins.str,
    ) -> "Node":
        '''(experimental) Find node within given **stack** with given *logicalId*.

        :param stack: -
        :param logical_id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52f242e9533d8e3603727048cefca8ca1bcd7283fbb68e8936a31f8e864f67be)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
        return typing.cast("Node", jsii.invoke(self, "findNodeByLogicalId", [stack, logical_id]))

    @jsii.member(jsii_name="findNodeByLogicalUniversalId")
    def find_node_by_logical_universal_id(self, uid: builtins.str) -> "Node":
        '''(experimental) Find node by **universal** *logicalId* (``<stack>:<logicalId>``).

        :param uid: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d15c19e972edf54940811c986029f8d06860695359ffc2b2989380610eeab001)
            check_type(argname="argument uid", value=uid, expected_type=type_hints["uid"])
        return typing.cast("Node", jsii.invoke(self, "findNodeByLogicalUniversalId", [uid]))

    @jsii.member(jsii_name="getEdge")
    def get_edge(self, uuid: builtins.str) -> "Edge":
        '''(experimental) Get stored **edge** by UUID.

        :param uuid: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7341fe8d2ac9a3e0b0f7460cb73d249ebdb7018202421d3652103d29f4036f53)
            check_type(argname="argument uuid", value=uuid, expected_type=type_hints["uuid"])
        return typing.cast("Edge", jsii.invoke(self, "getEdge", [uuid]))

    @jsii.member(jsii_name="getNode")
    def get_node(self, uuid: builtins.str) -> "Node":
        '''(experimental) Get stored **node** by UUID.

        :param uuid: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7172fc8d20040a0c391f68e341f9e854387e13c14ae068ebac677842b8124065)
            check_type(argname="argument uuid", value=uuid, expected_type=type_hints["uuid"])
        return typing.cast("Node", jsii.invoke(self, "getNode", [uuid]))

    @jsii.member(jsii_name="getStack")
    def get_stack(self, uuid: builtins.str) -> "StackNode":
        '''(experimental) Get stored **stack** node by UUID.

        :param uuid: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__016717b7d191ac618ce7ab95e30ef8a41c17d43bd9ee26a45afafe16d1256f43)
            check_type(argname="argument uuid", value=uuid, expected_type=type_hints["uuid"])
        return typing.cast("StackNode", jsii.invoke(self, "getStack", [uuid]))

    @jsii.member(jsii_name="getStage")
    def get_stage(self, uuid: builtins.str) -> "StageNode":
        '''(experimental) Get stored **stage** node by UUID.

        :param uuid: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fe9441b824214f582207d4a5c1dc9ee06de01c0bc48e2b6d064b4be3e80ce8f)
            check_type(argname="argument uuid", value=uuid, expected_type=type_hints["uuid"])
        return typing.cast("StageNode", jsii.invoke(self, "getStage", [uuid]))

    @jsii.member(jsii_name="mutateRemoveEdge")
    def mutate_remove_edge(self, edge: "Edge") -> builtins.bool:
        '''(experimental) Remove **edge** from the store.

        :param edge: -

        :stability: experimental
        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c44d23129ef772a7abc7b7904eedb0e3dbbe5ebfd71bcb42ad1a66ea0460faa4)
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
        return typing.cast(builtins.bool, jsii.invoke(self, "mutateRemoveEdge", [edge]))

    @jsii.member(jsii_name="mutateRemoveNode")
    def mutate_remove_node(self, node: "Node") -> builtins.bool:
        '''(experimental) Remove **node** from the store.

        :param node: -

        :stability: experimental
        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38f7f1a83926596fce68c62565a99f012d7bc267acf4a5a03b71046728afe3d6)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.invoke(self, "mutateRemoveNode", [node]))

    @jsii.member(jsii_name="recordImportArn")
    def record_import_arn(self, arn_token: builtins.str, resource: "Node") -> None:
        '''(experimental) Records arn tokens from imported resources (eg: ``s3.Bucket.fromBucketArn()``) that are used for resolving references.

        :param arn_token: -
        :param resource: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e82913f930cef17665caa74719684fe7d809e372cdf2e431606583476c790b3)
            check_type(argname="argument arn_token", value=arn_token, expected_type=type_hints["arn_token"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(None, jsii.invoke(self, "recordImportArn", [arn_token, resource]))

    @jsii.member(jsii_name="recordLogicalId")
    def record_logical_id(
        self,
        stack: "StackNode",
        logical_id: builtins.str,
        resource: "Node",
    ) -> None:
        '''(experimental) Record a **universal** *logicalId* to node mapping in the store.

        :param stack: -
        :param logical_id: -
        :param resource: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2998c0c7a2e8dcd67ac8d652f362598ce19a1470d35a293e301a2eb8c1bf538)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(None, jsii.invoke(self, "recordLogicalId", [stack, logical_id, resource]))

    @jsii.member(jsii_name="serialize")
    def serialize(self) -> SGGraphStore:
        '''(experimental) Serialize the store.

        :stability: experimental
        '''
        return typing.cast(SGGraphStore, jsii.invoke(self, "serialize", []))

    @jsii.member(jsii_name="verifyDestructiveMutationAllowed")
    def verify_destructive_mutation_allowed(self) -> None:
        '''(experimental) Verifies that the store allows destructive mutations.

        :stability: experimental
        :throws: Error is store does **not** allow mutations
        '''
        return typing.cast(None, jsii.invoke(self, "verifyDestructiveMutationAllowed", []))

    @builtins.property
    @jsii.member(jsii_name="allowDestructiveMutations")
    def allow_destructive_mutations(self) -> builtins.bool:
        '''(experimental) Indicates if the store allows destructive mutations.

        Destructive mutations are only allowed on clones of the store to prevent plugins and filters from
        mutating the store for downstream plugins.

        All ``mutate*`` methods are only allowed on stores that allow destructive mutations.

        This behavior may change in the future if the need arises for plugins to pass mutated stores
        to downstream plugins. But it will be done cautiously with ensuring the intent of
        downstream plugin is to receive the mutated store.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "allowDestructiveMutations"))

    @builtins.property
    @jsii.member(jsii_name="counts")
    def counts(self) -> IStoreCounts:
        '''(experimental) Get record of all store counters.

        :stability: experimental
        '''
        return typing.cast(IStoreCounts, jsii.get(self, "counts"))

    @builtins.property
    @jsii.member(jsii_name="edges")
    def edges(self) -> typing.List["Edge"]:
        '''(experimental) Gets all stored **edges**.

        :stability: experimental
        :type: ReadonlyArray
        '''
        return typing.cast(typing.List["Edge"], jsii.get(self, "edges"))

    @builtins.property
    @jsii.member(jsii_name="nodes")
    def nodes(self) -> typing.List["Node"]:
        '''(experimental) Gets all stored **nodes**.

        :stability: experimental
        :type: ReadonlyArray
        '''
        return typing.cast(typing.List["Node"], jsii.get(self, "nodes"))

    @builtins.property
    @jsii.member(jsii_name="root")
    def root(self) -> "RootNode":
        '''(experimental) Root node in the store.

        The **root** node is not the computed root, but the graph root
        which is auto-generated and can not be mutated.

        :stability: experimental
        '''
        return typing.cast("RootNode", jsii.get(self, "root"))

    @builtins.property
    @jsii.member(jsii_name="rootStacks")
    def root_stacks(self) -> typing.List["StackNode"]:
        '''(experimental) Gets all stored **root stack** nodes.

        :stability: experimental
        :type: ReadonlyArray
        '''
        return typing.cast(typing.List["StackNode"], jsii.get(self, "rootStacks"))

    @builtins.property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> typing.List["StackNode"]:
        '''(experimental) Gets all stored **stack** nodes.

        :stability: experimental
        :type: ReadonlyArray
        '''
        return typing.cast(typing.List["StackNode"], jsii.get(self, "stacks"))

    @builtins.property
    @jsii.member(jsii_name="stages")
    def stages(self) -> typing.List["StageNode"]:
        '''(experimental) Gets all stored **stage** nodes.

        :stability: experimental
        :type: ReadonlyArray
        '''
        return typing.cast(typing.List["StageNode"], jsii.get(self, "stages"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        '''(experimental) Current SemVer version of the store.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "version"))


@jsii.implements(ISerializableEntity)
class BaseEntity(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-prototyping-sdk/cdk-graph.BaseEntity",
):
    '''(experimental) Base class for all store entities (Node and Edges).

    :stability: experimental
    '''

    def __init__(self, props: IBaseEntityProps) -> None:
        '''
        :param props: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f2dc8f4d32f710e529c384ec54c4cf717f5cda309c0fbb212fcb4ec157460ec)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="addAttribute")
    def add_attribute(self, key: builtins.str, value: typing.Any) -> None:
        '''(experimental) Add attribute.

        :param key: -
        :param value: -

        :stability: experimental
        :throws: Error if attribute for key already exists
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fca287acaf0ea58ee6af4324bcf355d6fbcc074e558618b8b9aab6043f9cdc48)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addAttribute", [key, value]))

    @jsii.member(jsii_name="addFlag")
    def add_flag(self, flag: FlagEnum) -> None:
        '''(experimental) Add flag.

        :param flag: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9768f3202dfe93bb291e58985f3ddfcff7092cc72d09f07d2c7accffea6dc694)
            check_type(argname="argument flag", value=flag, expected_type=type_hints["flag"])
        return typing.cast(None, jsii.invoke(self, "addFlag", [flag]))

    @jsii.member(jsii_name="addMetadata")
    def add_metadata(self, metadata_type: builtins.str, data: typing.Any) -> None:
        '''(experimental) Add metadata entry.

        :param metadata_type: -
        :param data: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f98067f797cee431477c28fc9918bfc97075cec47a7b28b509fbbe24def0e110)
            check_type(argname="argument metadata_type", value=metadata_type, expected_type=type_hints["metadata_type"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
        return typing.cast(None, jsii.invoke(self, "addMetadata", [metadata_type, data]))

    @jsii.member(jsii_name="addTag")
    def add_tag(self, key: builtins.str, value: builtins.str) -> None:
        '''(experimental) Add tag.

        :param key: -
        :param value: -

        :stability: experimental
        :throws: Throws Error is tag for key already exists
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de490f4f63ecc3c4c21281b57fefef64c596b89d0a42c7832eed3312545b98a0)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addTag", [key, value]))

    @jsii.member(jsii_name="applyData")
    def apply_data(
        self,
        data: IBaseEntityDataProps,
        overwrite: typing.Optional[builtins.bool] = None,
        apply_flags: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Applies data (attributes, metadata, tags, flag) to entity.

        Generally used only for mutations such as collapse and consume to retain data.

        :param data: - The data to apply.
        :param overwrite: -
        :param apply_flags: - Indicates if data is overwritten - Indicates if flags should be applied.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__629d2e98b9f8de442a0a82d787ea97652535803463fe7587b1a46393f30ed41f)
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument overwrite", value=overwrite, expected_type=type_hints["overwrite"])
            check_type(argname="argument apply_flags", value=apply_flags, expected_type=type_hints["apply_flags"])
        return typing.cast(None, jsii.invoke(self, "applyData", [data, overwrite, apply_flags]))

    @jsii.member(jsii_name="findMetadata")
    def find_metadata(
        self,
        metadata_type: builtins.str,
    ) -> typing.List[_constructs_77d1e7e8.MetadataEntry]:
        '''(experimental) Retrieves all metadata entries of a given type.

        :param metadata_type: -

        :stability: experimental
        :type: Readonly<SerializedGraph.Metadata>
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c515cfd427885e594cc73e0ea60decf39cad8cd383f956aea551522a9607b37c)
            check_type(argname="argument metadata_type", value=metadata_type, expected_type=type_hints["metadata_type"])
        return typing.cast(typing.List[_constructs_77d1e7e8.MetadataEntry], jsii.invoke(self, "findMetadata", [metadata_type]))

    @jsii.member(jsii_name="getAttribute")
    def get_attribute(self, key: builtins.str) -> typing.Any:
        '''(experimental) Get attribute by key.

        :param key: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bb48787831bd62ba9cc6ec3cd4f437ccd2ca6b10c99437de64f5495a63fd95b)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast(typing.Any, jsii.invoke(self, "getAttribute", [key]))

    @jsii.member(jsii_name="getTag")
    def get_tag(self, key: builtins.str) -> typing.Optional[builtins.str]:
        '''(experimental) Get tag by key.

        :param key: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a90ad630d55a7c76dd403474c2f494d2e8b9e8ec9b19e11ff4058ba19f6ef1df)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "getTag", [key]))

    @jsii.member(jsii_name="hasAttribute")
    def has_attribute(
        self,
        key: builtins.str,
        value: typing.Any = None,
    ) -> builtins.bool:
        '''(experimental) Indicates if entity has a given attribute defined, and optionally with a specific value.

        :param key: -
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f7d28526dd59cd5f90985af0ba144e8702a6173d9b802954abd3282f2881676)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.bool, jsii.invoke(self, "hasAttribute", [key, value]))

    @jsii.member(jsii_name="hasFlag")
    def has_flag(self, flag: FlagEnum) -> builtins.bool:
        '''(experimental) Indicates if entity has a given flag.

        :param flag: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3740112f7f676b6a1901f67d18ecfbd6e0fb5275c0ae459d16bba2ac64eb0f1)
            check_type(argname="argument flag", value=flag, expected_type=type_hints["flag"])
        return typing.cast(builtins.bool, jsii.invoke(self, "hasFlag", [flag]))

    @jsii.member(jsii_name="hasMetadata")
    def has_metadata(
        self,
        metadata_type: builtins.str,
        data: typing.Any,
    ) -> builtins.bool:
        '''(experimental) Indicates if entity has matching metadata entry.

        :param metadata_type: -
        :param data: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff2f2591cae9b57daf46cbecf90260a471ad4c33792b0e2bb633a049e6bad804)
            check_type(argname="argument metadata_type", value=metadata_type, expected_type=type_hints["metadata_type"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
        return typing.cast(builtins.bool, jsii.invoke(self, "hasMetadata", [metadata_type, data]))

    @jsii.member(jsii_name="hasTag")
    def has_tag(
        self,
        key: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> builtins.bool:
        '''(experimental) Indicates if entity has tag, optionally verifying tag value.

        :param key: -
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffd521f5bd58d4907c987a3aafd2a00b78000a562aa35196fbee89ee1abedae6)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.bool, jsii.invoke(self, "hasTag", [key, value]))

    @jsii.member(jsii_name="mutateDestroy")
    @abc.abstractmethod
    def mutate_destroy(self, strict: typing.Optional[builtins.bool] = None) -> None:
        '''(experimental) Destroy the entity be removing all references and removing from store.

        :param strict: - If ``strict``, then entity must not have any references remaining when attempting to destroy.

        :stability: experimental
        :destructive: true
        '''
        ...

    @jsii.member(jsii_name="setAttribute")
    def set_attribute(self, key: builtins.str, value: typing.Any) -> None:
        '''(experimental) Set attribute.

        This will overwrite existing attribute.

        :param key: -
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61fb0de9c3c8ece2d2ee10210afc2406cd59f4f9003365b070efe806159b7e39)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "setAttribute", [key, value]))

    @jsii.member(jsii_name="setTag")
    def set_tag(self, key: builtins.str, value: builtins.str) -> None:
        '''(experimental) Set tag.

        Will overwrite existing tag.

        :param key: -
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ef46876bb2da2fab39362139ee1fa2ecf28ef8f4790d71956b03762c2858f9f)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "setTag", [key, value]))

    @builtins.property
    @jsii.member(jsii_name="attributes")
    def attributes(
        self,
    ) -> typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]]:
        '''(experimental) Get *readonly* record of all attributes.

        :stability: experimental
        :type: Readonly<SerializedGraph.Attributes>
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]], jsii.get(self, "attributes"))

    @builtins.property
    @jsii.member(jsii_name="flags")
    def flags(self) -> typing.List[FlagEnum]:
        '''(experimental) Get *readonly* list of all flags.

        :stability: experimental
        :type: ReadonlyArray
        '''
        return typing.cast(typing.List[FlagEnum], jsii.get(self, "flags"))

    @builtins.property
    @jsii.member(jsii_name="isDestroyed")
    def is_destroyed(self) -> builtins.bool:
        '''(experimental) Indicates if the entity has been destroyed (eg: removed from store).

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isDestroyed"))

    @builtins.property
    @jsii.member(jsii_name="isMutated")
    def is_mutated(self) -> builtins.bool:
        '''(experimental) Indicates if the entity has had destructive mutations applied.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isMutated"))

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.List[_constructs_77d1e7e8.MetadataEntry]:
        '''(experimental) Get *readonly* list of all metadata entries.

        :stability: experimental
        :type: Readonly<SerializedGraph.Metadata>
        '''
        return typing.cast(typing.List[_constructs_77d1e7e8.MetadataEntry], jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="store")
    def store(self) -> Store:
        '''(experimental) Reference to the store.

        :stability: experimental
        '''
        return typing.cast(Store, jsii.get(self, "store"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) Get *readonly* record of all tags.

        :stability: experimental
        :type: Readonly<SerializedGraph.Tags>
        '''
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="uuid")
    def uuid(self) -> builtins.str:
        '''(experimental) Universally unique identifier.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "uuid"))


class _BaseEntityProxy(BaseEntity):
    @jsii.member(jsii_name="mutateDestroy")
    def mutate_destroy(self, strict: typing.Optional[builtins.bool] = None) -> None:
        '''(experimental) Destroy the entity be removing all references and removing from store.

        :param strict: - If ``strict``, then entity must not have any references remaining when attempting to destroy.

        :stability: experimental
        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1b7b9c43f39c888d029ce6474749d13f8d3f6ea07e24ac2c73ede95e3d761ec)
            check_type(argname="argument strict", value=strict, expected_type=type_hints["strict"])
        return typing.cast(None, jsii.invoke(self, "mutateDestroy", [strict]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, BaseEntity).__jsii_proxy_class__ = lambda : _BaseEntityProxy


@jsii.implements(ISerializableEdge)
class Edge(
    BaseEntity,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-prototyping-sdk/cdk-graph.Edge",
):
    '''(experimental) Edge class defines a link (relationship) between nodes, as in standard `graph theory <https://en.wikipedia.org/wiki/Graph_theory>`_.

    :stability: experimental
    '''

    def __init__(self, props: "IEdgeProps") -> None:
        '''
        :param props: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc9940e76afa1f2a2a51af4a715cfc9ec8068b84e181427a075f3f950c7a75b4)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="findAllInChain")
    @builtins.classmethod
    def find_all_in_chain(
        cls,
        chain: typing.Sequence[typing.Any],
        predicate: IEdgePredicate,
    ) -> typing.List["Edge"]:
        '''(experimental) Find all matching edges based on predicate within an EdgeChain.

        :param chain: -
        :param predicate: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ba3c56cfbafe629bc5c97a1b8d94b2fa09bf263f48a13e19d3273aab0c213f5)
            check_type(argname="argument chain", value=chain, expected_type=type_hints["chain"])
            check_type(argname="argument predicate", value=predicate, expected_type=type_hints["predicate"])
        return typing.cast(typing.List["Edge"], jsii.sinvoke(cls, "findAllInChain", [chain, predicate]))

    @jsii.member(jsii_name="findInChain")
    @builtins.classmethod
    def find_in_chain(
        cls,
        chain: typing.Sequence[typing.Any],
        predicate: IEdgePredicate,
    ) -> typing.Optional["Edge"]:
        '''(experimental) Find first edge matching predicate within an EdgeChain.

        :param chain: -
        :param predicate: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d546855bb2ebbdf3c8f720ce8776a03968b65f340cea5fbbb408991981a9bb6)
            check_type(argname="argument chain", value=chain, expected_type=type_hints["chain"])
            check_type(argname="argument predicate", value=predicate, expected_type=type_hints["predicate"])
        return typing.cast(typing.Optional["Edge"], jsii.sinvoke(cls, "findInChain", [chain, predicate]))

    @jsii.member(jsii_name="isEquivalent")
    def is_equivalent(self, edge: "Edge") -> builtins.bool:
        '''(experimental) Indicates if this edge is equivalent to another edge.

        Edges are considered equivalent if they share same type, source, and target.

        :param edge: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c82d13d6d343f7daed5a05240546435a89e5e3beba9ca7e59942f57874a8a60)
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
        return typing.cast(builtins.bool, jsii.invoke(self, "isEquivalent", [edge]))

    @jsii.member(jsii_name="mutateConsume")
    def mutate_consume(self, edge: "Edge") -> None:
        '''(experimental) Merge an equivalent edge's data into this edge and destroy the other edge.

        Used during filtering operations to consolidate equivalent edges.

        :param edge: - The edge to consume.

        :stability: experimental
        :destructive: true
        :throws: Error is edge is not *equivalent*
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1806a9f734343b301c800fcc47acf0d01e612fca77d79b44938d9e1e3bde48ad)
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
        return typing.cast(None, jsii.invoke(self, "mutateConsume", [edge]))

    @jsii.member(jsii_name="mutateDestroy")
    def mutate_destroy(self, _strict: typing.Optional[builtins.bool] = None) -> None:
        '''(experimental) Destroy the edge.

        Remove all references and remove from store.

        :param _strict: -

        :stability: experimental
        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c054019cea048023a1223d0f4340b9012468fa648505eaeb18f3a309574034c4)
            check_type(argname="argument _strict", value=_strict, expected_type=type_hints["_strict"])
        return typing.cast(None, jsii.invoke(self, "mutateDestroy", [_strict]))

    @jsii.member(jsii_name="mutateDirection")
    def mutate_direction(self, direction: EdgeDirectionEnum) -> None:
        '''(experimental) Change the edge **direction**.

        :param direction: -

        :stability: experimental
        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9381ac56f06abe54b86023ee566cee97fbe66d927f289a01c168fa96bdc89be4)
            check_type(argname="argument direction", value=direction, expected_type=type_hints["direction"])
        return typing.cast(None, jsii.invoke(self, "mutateDirection", [direction]))

    @jsii.member(jsii_name="mutateSource")
    def mutate_source(self, node: "Node") -> None:
        '''(experimental) Change the edge **source**.

        :param node: -

        :stability: experimental
        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__725116b7334022c2e38d2495b1c2fea7a1a1e3bfce318823076d2d73e32b4e2b)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "mutateSource", [node]))

    @jsii.member(jsii_name="mutateTarget")
    def mutate_target(self, node: "Node") -> None:
        '''(experimental) Change the edge **target**.

        :param node: -

        :stability: experimental
        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f074e21e7d8f7ba613f207b1351316f3834cc0276f4d34070b3f84fc73ca6de2)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "mutateTarget", [node]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Get string representation of this edge.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="allowDestructiveMutations")
    def allow_destructive_mutations(self) -> builtins.bool:
        '''(experimental) Indicates if edge allows destructive mutations.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "allowDestructiveMutations"))

    @builtins.property
    @jsii.member(jsii_name="direction")
    def direction(self) -> EdgeDirectionEnum:
        '''(experimental) Indicates the direction in which the edge is directed.

        :stability: experimental
        '''
        return typing.cast(EdgeDirectionEnum, jsii.get(self, "direction"))

    @builtins.property
    @jsii.member(jsii_name="edgeType")
    def edge_type(self) -> EdgeTypeEnum:
        '''(experimental) Type of edge.

        :stability: experimental
        '''
        return typing.cast(EdgeTypeEnum, jsii.get(self, "edgeType"))

    @builtins.property
    @jsii.member(jsii_name="isClosed")
    def is_closed(self) -> builtins.bool:
        '''(experimental) Indicates if the Edge's **source** and **target** are the same, or were the same when it was created (prior to mutations).

        To check whether it was originally closed, use ``hasFlag(FlagEnum.CLOSED_EDGE)`` instead.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isClosed"))

    @builtins.property
    @jsii.member(jsii_name="isCrossStack")
    def is_cross_stack(self) -> builtins.bool:
        '''(experimental) Indicates if **source** and **target** nodes reside in different *root* stacks.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isCrossStack"))

    @builtins.property
    @jsii.member(jsii_name="isExtraneous")
    def is_extraneous(self) -> builtins.bool:
        '''(experimental) Indicates if edge is extraneous which is determined by explicitly having *EXTRANEOUS* flag added and/or being a closed loop (source===target).

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isExtraneous"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> "Node":
        '''(experimental) Edge **source** is the node that defines the edge (tail).

        :stability: experimental
        '''
        return typing.cast("Node", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "Node":
        '''(experimental) Edge **target** is the node being referenced by the **source** (head).

        :stability: experimental
        '''
        return typing.cast("Node", jsii.get(self, "target"))


@jsii.interface(jsii_type="@aws-prototyping-sdk/cdk-graph.IAppNodeProps")
class IAppNodeProps(IBaseEntityDataProps, typing_extensions.Protocol):
    '''(experimental) {@link AppNode} props.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="store")
    def store(self) -> Store:
        '''(experimental) Store.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="cfnType")
    def cfn_type(self) -> typing.Optional[builtins.str]:
        '''(experimental) Type of CloudFormation resource.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="constructInfo")
    def construct_info(self) -> typing.Optional[ConstructInfo]:
        '''(experimental) Synthesized construct information defining jii resolution data.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="logicalId")
    def logical_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) Logical id of the node, which is only unique within containing stack.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> typing.Optional["Node"]:
        '''(experimental) Parent node.

        :stability: experimental
        '''
        ...


class _IAppNodePropsProxy(
    jsii.proxy_for(IBaseEntityDataProps), # type: ignore[misc]
):
    '''(experimental) {@link AppNode} props.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph.IAppNodeProps"

    @builtins.property
    @jsii.member(jsii_name="store")
    def store(self) -> Store:
        '''(experimental) Store.

        :stability: experimental
        '''
        return typing.cast(Store, jsii.get(self, "store"))

    @builtins.property
    @jsii.member(jsii_name="cfnType")
    def cfn_type(self) -> typing.Optional[builtins.str]:
        '''(experimental) Type of CloudFormation resource.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cfnType"))

    @builtins.property
    @jsii.member(jsii_name="constructInfo")
    def construct_info(self) -> typing.Optional[ConstructInfo]:
        '''(experimental) Synthesized construct information defining jii resolution data.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[ConstructInfo], jsii.get(self, "constructInfo"))

    @builtins.property
    @jsii.member(jsii_name="logicalId")
    def logical_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) Logical id of the node, which is only unique within containing stack.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logicalId"))

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> typing.Optional["Node"]:
        '''(experimental) Parent node.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["Node"], jsii.get(self, "parent"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAppNodeProps).__jsii_proxy_class__ = lambda : _IAppNodePropsProxy


@jsii.interface(jsii_type="@aws-prototyping-sdk/cdk-graph.IAttributeReferenceProps")
class IAttributeReferenceProps(ITypedEdgeProps, typing_extensions.Protocol):
    '''(experimental) Attribute type reference props.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(
        self,
    ) -> typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]:
        '''(experimental) Resolved attribute value.

        :stability: experimental
        '''
        ...

    @value.setter
    def value(
        self,
        value: typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]],
    ) -> None:
        ...


class _IAttributeReferencePropsProxy(
    jsii.proxy_for(ITypedEdgeProps), # type: ignore[misc]
):
    '''(experimental) Attribute type reference props.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph.IAttributeReferenceProps"

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(
        self,
    ) -> typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]:
        '''(experimental) Resolved attribute value.

        :stability: experimental
        '''
        return typing.cast(typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]], jsii.get(self, "value"))

    @value.setter
    def value(
        self,
        value: typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b19f3c99c1010b7e42cbb686da8f9795320e98e9f3a0384ef6e4c6d29f33d2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAttributeReferenceProps).__jsii_proxy_class__ = lambda : _IAttributeReferencePropsProxy


@jsii.interface(jsii_type="@aws-prototyping-sdk/cdk-graph.ICfnResourceNodeProps")
class ICfnResourceNodeProps(ITypedNodeProps, typing_extensions.Protocol):
    '''(experimental) CfnResourceNode props.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="importArnToken")
    def import_arn_token(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        ...

    @import_arn_token.setter
    def import_arn_token(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> typing.Optional[NodeTypeEnum]:
        '''
        :stability: experimental
        '''
        ...

    @node_type.setter
    def node_type(self, value: typing.Optional[NodeTypeEnum]) -> None:
        ...


class _ICfnResourceNodePropsProxy(
    jsii.proxy_for(ITypedNodeProps), # type: ignore[misc]
):
    '''(experimental) CfnResourceNode props.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph.ICfnResourceNodeProps"

    @builtins.property
    @jsii.member(jsii_name="importArnToken")
    def import_arn_token(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "importArnToken"))

    @import_arn_token.setter
    def import_arn_token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34855dc7b232fc8d813a1b62cdcdd54bcbb46b14402f35ecd54aab1f79be69a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "importArnToken", value)

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> typing.Optional[NodeTypeEnum]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[NodeTypeEnum], jsii.get(self, "nodeType"))

    @node_type.setter
    def node_type(self, value: typing.Optional[NodeTypeEnum]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2e86175e2d1b5d420625acfdb4a456691dd03d9008fbcf378db33eecd318cfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeType", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICfnResourceNodeProps).__jsii_proxy_class__ = lambda : _ICfnResourceNodePropsProxy


@jsii.interface(jsii_type="@aws-prototyping-sdk/cdk-graph.IEdgeProps")
class IEdgeProps(ITypedEdgeProps, typing_extensions.Protocol):
    '''(experimental) Edge props interface.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="direction")
    def direction(self) -> EdgeDirectionEnum:
        '''(experimental) Indicates the direction in which the edge is directed.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="edgeType")
    def edge_type(self) -> EdgeTypeEnum:
        '''(experimental) Type of edge.

        :stability: experimental
        '''
        ...


class _IEdgePropsProxy(
    jsii.proxy_for(ITypedEdgeProps), # type: ignore[misc]
):
    '''(experimental) Edge props interface.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph.IEdgeProps"

    @builtins.property
    @jsii.member(jsii_name="direction")
    def direction(self) -> EdgeDirectionEnum:
        '''(experimental) Indicates the direction in which the edge is directed.

        :stability: experimental
        '''
        return typing.cast(EdgeDirectionEnum, jsii.get(self, "direction"))

    @builtins.property
    @jsii.member(jsii_name="edgeType")
    def edge_type(self) -> EdgeTypeEnum:
        '''(experimental) Type of edge.

        :stability: experimental
        '''
        return typing.cast(EdgeTypeEnum, jsii.get(self, "edgeType"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IEdgeProps).__jsii_proxy_class__ = lambda : _IEdgePropsProxy


@jsii.interface(jsii_type="@aws-prototyping-sdk/cdk-graph.INodeProps")
class INodeProps(ITypedNodeProps, typing_extensions.Protocol):
    '''(experimental) Node props.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> NodeTypeEnum:
        '''(experimental) Type of node.

        :stability: experimental
        '''
        ...


class _INodePropsProxy(
    jsii.proxy_for(ITypedNodeProps), # type: ignore[misc]
):
    '''(experimental) Node props.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph.INodeProps"

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> NodeTypeEnum:
        '''(experimental) Type of node.

        :stability: experimental
        '''
        return typing.cast(NodeTypeEnum, jsii.get(self, "nodeType"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INodeProps).__jsii_proxy_class__ = lambda : _INodePropsProxy


@jsii.interface(jsii_type="@aws-prototyping-sdk/cdk-graph.IOutputNodeProps")
class IOutputNodeProps(ITypedNodeProps, typing_extensions.Protocol):
    '''(experimental) OutputNode props.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Any:
        '''(experimental) Resolved output value.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="exportName")
    def export_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Export name.

        :stability: experimental
        '''
        ...


class _IOutputNodePropsProxy(
    jsii.proxy_for(ITypedNodeProps), # type: ignore[misc]
):
    '''(experimental) OutputNode props.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph.IOutputNodeProps"

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Any:
        '''(experimental) Resolved output value.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="exportName")
    def export_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Export name.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exportName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IOutputNodeProps).__jsii_proxy_class__ = lambda : _IOutputNodePropsProxy


@jsii.interface(jsii_type="@aws-prototyping-sdk/cdk-graph.IParameterNodeProps")
class IParameterNodeProps(ITypedNodeProps, typing_extensions.Protocol):
    '''(experimental) {@link ParameterNode} props.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="parameterType")
    def parameter_type(self) -> builtins.str:
        '''(experimental) Parameter type.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Any:
        '''(experimental) Resolved value.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description.

        :stability: experimental
        '''
        ...


class _IParameterNodePropsProxy(
    jsii.proxy_for(ITypedNodeProps), # type: ignore[misc]
):
    '''(experimental) {@link ParameterNode} props.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph.IParameterNodeProps"

    @builtins.property
    @jsii.member(jsii_name="parameterType")
    def parameter_type(self) -> builtins.str:
        '''(experimental) Parameter type.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "parameterType"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Any:
        '''(experimental) Resolved value.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IParameterNodeProps).__jsii_proxy_class__ = lambda : _IParameterNodePropsProxy


@jsii.interface(jsii_type="@aws-prototyping-sdk/cdk-graph.IReferenceProps")
class IReferenceProps(ITypedEdgeProps, typing_extensions.Protocol):
    '''(experimental) Reference edge props.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="referenceType")
    def reference_type(self) -> typing.Optional[ReferenceTypeEnum]:
        '''(experimental) Type of reference.

        :stability: experimental
        '''
        ...

    @reference_type.setter
    def reference_type(self, value: typing.Optional[ReferenceTypeEnum]) -> None:
        ...


class _IReferencePropsProxy(
    jsii.proxy_for(ITypedEdgeProps), # type: ignore[misc]
):
    '''(experimental) Reference edge props.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph.IReferenceProps"

    @builtins.property
    @jsii.member(jsii_name="referenceType")
    def reference_type(self) -> typing.Optional[ReferenceTypeEnum]:
        '''(experimental) Type of reference.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[ReferenceTypeEnum], jsii.get(self, "referenceType"))

    @reference_type.setter
    def reference_type(self, value: typing.Optional[ReferenceTypeEnum]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59d7bc44379b4c689592001d4e5ab142c8f56c533b1ce7da958b1f9a0e3c0149)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "referenceType", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IReferenceProps).__jsii_proxy_class__ = lambda : _IReferencePropsProxy


@jsii.interface(jsii_type="@aws-prototyping-sdk/cdk-graph.IResourceNodeProps")
class IResourceNodeProps(ITypedNodeProps, typing_extensions.Protocol):
    '''(experimental) ResourceNode props.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="cdkOwned")
    def cdk_owned(self) -> builtins.bool:
        '''(experimental) Indicates if this resource is owned by cdk (defined in cdk library).

        :stability: experimental
        '''
        ...

    @cdk_owned.setter
    def cdk_owned(self, value: builtins.bool) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> typing.Optional[NodeTypeEnum]:
        '''(experimental) Type of node.

        :stability: experimental
        '''
        ...

    @node_type.setter
    def node_type(self, value: typing.Optional[NodeTypeEnum]) -> None:
        ...


class _IResourceNodePropsProxy(
    jsii.proxy_for(ITypedNodeProps), # type: ignore[misc]
):
    '''(experimental) ResourceNode props.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph.IResourceNodeProps"

    @builtins.property
    @jsii.member(jsii_name="cdkOwned")
    def cdk_owned(self) -> builtins.bool:
        '''(experimental) Indicates if this resource is owned by cdk (defined in cdk library).

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "cdkOwned"))

    @cdk_owned.setter
    def cdk_owned(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26cde6447d66f5a35ac630eb24e426e3c519cb621e706720d313cd85ca412122)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cdkOwned", value)

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> typing.Optional[NodeTypeEnum]:
        '''(experimental) Type of node.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[NodeTypeEnum], jsii.get(self, "nodeType"))

    @node_type.setter
    def node_type(self, value: typing.Optional[NodeTypeEnum]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14ac61e4840795aa21b772948740dfece254d05e6c034663ae54ca236dcd015d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeType", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IResourceNodeProps).__jsii_proxy_class__ = lambda : _IResourceNodePropsProxy


@jsii.interface(jsii_type="@aws-prototyping-sdk/cdk-graph.IStackNodeProps")
class IStackNodeProps(ITypedNodeProps, typing_extensions.Protocol):
    '''(experimental) {@link StackNode} props.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> typing.Optional[NodeTypeEnum]:
        '''(experimental) Type of node.

        :stability: experimental
        '''
        ...

    @node_type.setter
    def node_type(self, value: typing.Optional[NodeTypeEnum]) -> None:
        ...


class _IStackNodePropsProxy(
    jsii.proxy_for(ITypedNodeProps), # type: ignore[misc]
):
    '''(experimental) {@link StackNode} props.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph.IStackNodeProps"

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> typing.Optional[NodeTypeEnum]:
        '''(experimental) Type of node.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[NodeTypeEnum], jsii.get(self, "nodeType"))

    @node_type.setter
    def node_type(self, value: typing.Optional[NodeTypeEnum]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcdd9af99464b5c5d6c5f4a91b9bfd01b43db3776a90c811162abfcf1dd1e197)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeType", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IStackNodeProps).__jsii_proxy_class__ = lambda : _IStackNodePropsProxy


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/cdk-graph.InferredNodeProps",
    jsii_struct_bases=[SGEntity],
    name_mapping={
        "uuid": "uuid",
        "attributes": "attributes",
        "flags": "flags",
        "metadata": "metadata",
        "tags": "tags",
        "dependencies": "dependencies",
        "unresolved_references": "unresolvedReferences",
        "cfn_type": "cfnType",
        "construct_info": "constructInfo",
        "logical_id": "logicalId",
    },
)
class InferredNodeProps(SGEntity):
    def __init__(
        self,
        *,
        uuid: builtins.str,
        attributes: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]]]]]]] = None,
        flags: typing.Optional[typing.Sequence[FlagEnum]] = None,
        metadata: typing.Optional[typing.Sequence[typing.Union[_constructs_77d1e7e8.MetadataEntry, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        dependencies: typing.Sequence[builtins.str],
        unresolved_references: typing.Sequence[typing.Union[SGUnresolvedReference, typing.Dict[builtins.str, typing.Any]]],
        cfn_type: typing.Optional[builtins.str] = None,
        construct_info: typing.Optional[typing.Union[ConstructInfo, typing.Dict[builtins.str, typing.Any]]] = None,
        logical_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Inferred node props.

        :param uuid: (experimental) Universally unique identity.
        :param attributes: (experimental) Serializable entity attributes.
        :param flags: (experimental) Serializable entity flags.
        :param metadata: (experimental) Serializable entity metadata.
        :param tags: (experimental) Serializable entity tags.
        :param dependencies: 
        :param unresolved_references: 
        :param cfn_type: 
        :param construct_info: 
        :param logical_id: 

        :stability: experimental
        '''
        if isinstance(construct_info, dict):
            construct_info = ConstructInfo(**construct_info)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc702434f9098ad5400a36b4d5fa85826622b6657d1dd0f3392de0bcab361f2c)
            check_type(argname="argument uuid", value=uuid, expected_type=type_hints["uuid"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument flags", value=flags, expected_type=type_hints["flags"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument dependencies", value=dependencies, expected_type=type_hints["dependencies"])
            check_type(argname="argument unresolved_references", value=unresolved_references, expected_type=type_hints["unresolved_references"])
            check_type(argname="argument cfn_type", value=cfn_type, expected_type=type_hints["cfn_type"])
            check_type(argname="argument construct_info", value=construct_info, expected_type=type_hints["construct_info"])
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uuid": uuid,
            "dependencies": dependencies,
            "unresolved_references": unresolved_references,
        }
        if attributes is not None:
            self._values["attributes"] = attributes
        if flags is not None:
            self._values["flags"] = flags
        if metadata is not None:
            self._values["metadata"] = metadata
        if tags is not None:
            self._values["tags"] = tags
        if cfn_type is not None:
            self._values["cfn_type"] = cfn_type
        if construct_info is not None:
            self._values["construct_info"] = construct_info
        if logical_id is not None:
            self._values["logical_id"] = logical_id

    @builtins.property
    def uuid(self) -> builtins.str:
        '''(experimental) Universally unique identity.

        :stability: experimental
        '''
        result = self._values.get("uuid")
        assert result is not None, "Required property 'uuid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]]]:
        '''(experimental) Serializable entity attributes.

        :see: {@link Attributes }
        :stability: experimental
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]]], result)

    @builtins.property
    def flags(self) -> typing.Optional[typing.List[FlagEnum]]:
        '''(experimental) Serializable entity flags.

        :see: {@link FlagEnum }
        :stability: experimental
        '''
        result = self._values.get("flags")
        return typing.cast(typing.Optional[typing.List[FlagEnum]], result)

    @builtins.property
    def metadata(
        self,
    ) -> typing.Optional[typing.List[_constructs_77d1e7e8.MetadataEntry]]:
        '''(experimental) Serializable entity metadata.

        :see: {@link Metadata }
        :stability: experimental
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.List[_constructs_77d1e7e8.MetadataEntry]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Serializable entity tags.

        :see: {@link Tags }
        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def dependencies(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("dependencies")
        assert result is not None, "Required property 'dependencies' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def unresolved_references(self) -> typing.List[SGUnresolvedReference]:
        '''
        :stability: experimental
        '''
        result = self._values.get("unresolved_references")
        assert result is not None, "Required property 'unresolved_references' is missing"
        return typing.cast(typing.List[SGUnresolvedReference], result)

    @builtins.property
    def cfn_type(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("cfn_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def construct_info(self) -> typing.Optional[ConstructInfo]:
        '''
        :stability: experimental
        '''
        result = self._values.get("construct_info")
        return typing.cast(typing.Optional[ConstructInfo], result)

    @builtins.property
    def logical_id(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("logical_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InferredNodeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ISerializableNode)
class Node(
    BaseEntity,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-prototyping-sdk/cdk-graph.Node",
):
    '''(experimental) Node class is the base definition of **node** entities in the graph, as in standard `graph theory <https://en.wikipedia.org/wiki/Graph_theory>`_.

    :stability: experimental
    '''

    def __init__(self, props: INodeProps) -> None:
        '''
        :param props: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74fba1b214a0b6da2c81857be0f084091ee35bd210c9a55c3fd5e104e3e0dec4)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="addChild")
    def add_child(self, node: "Node") -> None:
        '''(experimental) Add *child* node.

        :param node: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3da87100250635b0c50af6bdcd03a86edd18d0aac4df75ad9acc23cb03167b76)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "addChild", [node]))

    @jsii.member(jsii_name="addLink")
    def add_link(self, edge: Edge) -> None:
        '''(experimental) Add *link* to another node.

        :param edge: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fecabe827c1e09a7a8c0b545f904fd63ceded0137ef9c59c283bad92192b8779)
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
        return typing.cast(None, jsii.invoke(self, "addLink", [edge]))

    @jsii.member(jsii_name="addReverseLink")
    def add_reverse_link(self, edge: Edge) -> None:
        '''(experimental) Add *link* from another node.

        :param edge: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f652daee515413ba0e936bdd57028711a6f6d1e07a4732025f7a58047ee1f599)
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
        return typing.cast(None, jsii.invoke(self, "addReverseLink", [edge]))

    @jsii.member(jsii_name="doesDependOn")
    def does_depend_on(self, node: "Node") -> builtins.bool:
        '''(experimental) Indicates if *this node* depends on *another node*.

        :param node: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8fce1a47ea1104d69fc39fdeaf2352f4c88133185dff4b085c03fdcdd5cf4de)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.invoke(self, "doesDependOn", [node]))

    @jsii.member(jsii_name="doesReference")
    def does_reference(self, node: "Node") -> builtins.bool:
        '''(experimental) Indicates if *this node* references *another node*.

        :param node: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d30c20ae909df3aaed77d3c61ddb29622905d2cf8b95df8eb73d4f7cc5fe4a9a)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.invoke(self, "doesReference", [node]))

    @jsii.member(jsii_name="find")
    def find(self, predicate: INodePredicate) -> typing.Optional["Node"]:
        '''(experimental) Recursively find the nearest sub-node matching predicate.

        :param predicate: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5987c16db88320ba918a789572bee8884821f66266adc3461833f3808b51611)
            check_type(argname="argument predicate", value=predicate, expected_type=type_hints["predicate"])
        return typing.cast(typing.Optional["Node"], jsii.invoke(self, "find", [predicate]))

    @jsii.member(jsii_name="findAll")
    def find_all(
        self,
        options: typing.Optional[IFindNodeOptions] = None,
    ) -> typing.List["Node"]:
        '''(experimental) Return this construct and all of its sub-nodes in the given order.

        Optionally filter nodes based on predicate.

        :param options: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68abed2aa07ec0b51cf326a6d40ccc90857dcc58aa8602d6fe3a4c95428f7529)
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
        return typing.cast(typing.List["Node"], jsii.invoke(self, "findAll", [options]))

    @jsii.member(jsii_name="findAllLinks")
    def find_all_links(
        self,
        options: typing.Optional[IFindEdgeOptions] = None,
    ) -> typing.List[Edge]:
        '''(experimental) Return all direct links of this node and that of all sub-nodes.

        Optionally filter links based on predicate.

        :param options: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7f0f74c30a800cda16150fb9dd37ffff3569b44fb0decf754a0b52b58fb0216)
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
        return typing.cast(typing.List[Edge], jsii.invoke(self, "findAllLinks", [options]))

    @jsii.member(jsii_name="findAncestor")
    def find_ancestor(
        self,
        predicate: INodePredicate,
        max: typing.Optional[jsii.Number] = None,
    ) -> typing.Optional["Node"]:
        '''(experimental) Find nearest *ancestor* of *this node* matching given predicate.

        :param predicate: - Predicate to match ancestor.
        :param max: -

        :stability: experimental
        :max: {number} [max] - Optional maximum levels to ascend
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c48bf8b6d829071f27f765fa51569e4816e62af749fb1380a1adb9b327209649)
            check_type(argname="argument predicate", value=predicate, expected_type=type_hints["predicate"])
            check_type(argname="argument max", value=max, expected_type=type_hints["max"])
        return typing.cast(typing.Optional["Node"], jsii.invoke(self, "findAncestor", [predicate, max]))

    @jsii.member(jsii_name="findChild")
    def find_child(self, id: builtins.str) -> typing.Optional["Node"]:
        '''(experimental) Find child with given *id*.

        Similar to ``find`` but does not throw error if no child found.

        :param id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1250fde13da19383a24377937a8e3da9c1dac10eaf648f088df319d8d95aaf5)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast(typing.Optional["Node"], jsii.invoke(self, "findChild", [id]))

    @jsii.member(jsii_name="findLink")
    def find_link(
        self,
        predicate: IEdgePredicate,
        reverse: typing.Optional[builtins.bool] = None,
        follow: typing.Optional[builtins.bool] = None,
        direct: typing.Optional[builtins.bool] = None,
    ) -> typing.Optional[Edge]:
        '''(experimental) Find link of this node based on predicate.

        By default this will follow link
        chains to evaluate the predicate against and return the matching direct link
        of this node.

        :param predicate: Edge predicate function to match edge.
        :param reverse: Indicates if links are search in reverse order.
        :param follow: Indicates if link chain is followed.
        :param direct: Indicates that only *direct* links should be searched.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6751959dbf5836b0001e27458851fb4102db4a1cd85ed0612c9609062b59e1d8)
            check_type(argname="argument predicate", value=predicate, expected_type=type_hints["predicate"])
            check_type(argname="argument reverse", value=reverse, expected_type=type_hints["reverse"])
            check_type(argname="argument follow", value=follow, expected_type=type_hints["follow"])
            check_type(argname="argument direct", value=direct, expected_type=type_hints["direct"])
        return typing.cast(typing.Optional[Edge], jsii.invoke(self, "findLink", [predicate, reverse, follow, direct]))

    @jsii.member(jsii_name="findLinks")
    def find_links(
        self,
        predicate: IEdgePredicate,
        reverse: typing.Optional[builtins.bool] = None,
        follow: typing.Optional[builtins.bool] = None,
        direct: typing.Optional[builtins.bool] = None,
    ) -> typing.List[Edge]:
        '''(experimental) Find all links of this node based on predicate.

        By default this will follow link
        chains to evaluate the predicate against and return the matching direct links
        of this node.

        :param predicate: Edge predicate function to match edge.
        :param reverse: Indicates if links are search in reverse order.
        :param follow: Indicates if link chain is followed.
        :param direct: Indicates that only *direct* links should be searched.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb69053fa918bf283e62a41638c10b714ca12d8a7c133e8eff448d274828f91e)
            check_type(argname="argument predicate", value=predicate, expected_type=type_hints["predicate"])
            check_type(argname="argument reverse", value=reverse, expected_type=type_hints["reverse"])
            check_type(argname="argument follow", value=follow, expected_type=type_hints["follow"])
            check_type(argname="argument direct", value=direct, expected_type=type_hints["direct"])
        return typing.cast(typing.List[Edge], jsii.invoke(self, "findLinks", [predicate, reverse, follow, direct]))

    @jsii.member(jsii_name="getCfnProp")
    def get_cfn_prop(
        self,
        key: builtins.str,
    ) -> typing.Optional[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]]:
        '''(experimental) Get specific CloudFormation property.

        :param key: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a71ef48e84e46dc216625c429813b383dfdcdf3dcbaa7da531fa9f8a8b95d8a3)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast(typing.Optional[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]], jsii.invoke(self, "getCfnProp", [key]))

    @jsii.member(jsii_name="getChild")
    def get_child(self, id: builtins.str) -> "Node":
        '''(experimental) Get *child* node with given *id*.

        :param id: -

        :stability: experimental
        :throws: Error if no child with given id
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4ad2e0d7a748a08d49142472755ec0a258b78c24707aa0873d4eb150abb5c74)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast("Node", jsii.invoke(self, "getChild", [id]))

    @jsii.member(jsii_name="getLinkChains")
    def get_link_chains(
        self,
        reverse: typing.Optional[builtins.bool] = None,
    ) -> typing.List[typing.List[typing.Any]]:
        '''(experimental) Resolve all link chains.

        :param reverse: -

        :see: {@link EdgeChain }
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aa874e5b7d5b668ae367553a55f5db22d91f39d582e443f65eeb7b8b8e21e85)
            check_type(argname="argument reverse", value=reverse, expected_type=type_hints["reverse"])
        return typing.cast(typing.List[typing.List[typing.Any]], jsii.invoke(self, "getLinkChains", [reverse]))

    @jsii.member(jsii_name="getNearestAncestor")
    def get_nearest_ancestor(self, node: "Node") -> "Node":
        '''(experimental) Gets the nearest **common** *ancestor* shared between *this node* and another *node*.

        :param node: -

        :stability: experimental
        :throws: Error if *node* does not share a **common** *ancestor*
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea903bfc5fb1ce19d9fb323a51a92834bd520d5834c12419ee4fddeb0d750330)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast("Node", jsii.invoke(self, "getNearestAncestor", [node]))

    @jsii.member(jsii_name="isAncestor")
    def is_ancestor(self, ancestor: "Node") -> builtins.bool:
        '''(experimental) Indicates if a specific *node* is an *ancestor* of *this node*.

        :param ancestor: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0b1c27a0709375706f73127e248dfbda0cbab1ead7faf39dfe11be7a1226cfc)
            check_type(argname="argument ancestor", value=ancestor, expected_type=type_hints["ancestor"])
        return typing.cast(builtins.bool, jsii.invoke(self, "isAncestor", [ancestor]))

    @jsii.member(jsii_name="isChild")
    def is_child(self, node: "Node") -> builtins.bool:
        '''(experimental) Indicates if specific *node* is a *child* of *this node*.

        :param node: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bd700d653ffb5a3352a6639c715f3cb25552651b3504110d9d3fb9583c9c233)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.invoke(self, "isChild", [node]))

    @jsii.member(jsii_name="mutateCollapse")
    def mutate_collapse(self) -> None:
        '''(experimental) Collapses all sub-nodes of *this node* into *this node*.

        :stability: experimental
        :destructive: true
        '''
        return typing.cast(None, jsii.invoke(self, "mutateCollapse", []))

    @jsii.member(jsii_name="mutateCollapseTo")
    def mutate_collapse_to(self, ancestor: "Node") -> "Node":
        '''(experimental) Collapses *this node* into *an ancestor*.

        :param ancestor: -

        :stability: experimental
        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2575a885febef02fb0b0e973913fe6b8ee79fdba778ca87f62f1b1c83b2bfe0)
            check_type(argname="argument ancestor", value=ancestor, expected_type=type_hints["ancestor"])
        return typing.cast("Node", jsii.invoke(self, "mutateCollapseTo", [ancestor]))

    @jsii.member(jsii_name="mutateCollapseToParent")
    def mutate_collapse_to_parent(self) -> "Node":
        '''(experimental) Collapses *this node* into *it's parent node*.

        :stability: experimental
        :destructive: true
        '''
        return typing.cast("Node", jsii.invoke(self, "mutateCollapseToParent", []))

    @jsii.member(jsii_name="mutateDestroy")
    def mutate_destroy(self, strict: typing.Optional[builtins.bool] = None) -> None:
        '''(experimental) Destroys this node by removing all references and removing this node from the store.

        :param strict: - Indicates that this node must not have references.

        :stability: experimental
        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9b18468fcf94a48458d4d3eeb8cfde1c9322a2508820c8ada0cc9e48a8a8658)
            check_type(argname="argument strict", value=strict, expected_type=type_hints["strict"])
        return typing.cast(None, jsii.invoke(self, "mutateDestroy", [strict]))

    @jsii.member(jsii_name="mutateHoist")
    def mutate_hoist(self, new_parent: "Node") -> None:
        '''(experimental) Hoist *this node* to an *ancestor* by removing it from its current parent node and in turn moving it to the ancestor.

        :param new_parent: -

        :stability: experimental
        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d56c8215efb5ab6998320a2aa4edaa2cf82014505476153fb15524d6cc65441c)
            check_type(argname="argument new_parent", value=new_parent, expected_type=type_hints["new_parent"])
        return typing.cast(None, jsii.invoke(self, "mutateHoist", [new_parent]))

    @jsii.member(jsii_name="mutateMove")
    def mutate_move(self, new_parent: "Node") -> None:
        '''(experimental) Move this node into a new parent node.

        :param new_parent: - The parent to move this node to.

        :stability: experimental
        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deada882d081798a49ca7dadca89fbf1032b8eb25cdc7f98541af185cd7fe5cf)
            check_type(argname="argument new_parent", value=new_parent, expected_type=type_hints["new_parent"])
        return typing.cast(None, jsii.invoke(self, "mutateMove", [new_parent]))

    @jsii.member(jsii_name="mutateRemoveChild")
    def mutate_remove_child(self, node: "Node") -> builtins.bool:
        '''(experimental) Remove a *child* node from *this node*.

        :param node: -

        :stability: experimental
        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9054f48201348fe56a5b872785512bfc264c9b97152917a97ec019d68ef6890)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.invoke(self, "mutateRemoveChild", [node]))

    @jsii.member(jsii_name="mutateRemoveLink")
    def mutate_remove_link(self, link: Edge) -> builtins.bool:
        '''(experimental) Remove a *link* from *this node*.

        :param link: -

        :stability: experimental
        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6dd90ba9fb9c195c8498aa32ac50c1e8008d173cb87ed535f21dbe835ff1309)
            check_type(argname="argument link", value=link, expected_type=type_hints["link"])
        return typing.cast(builtins.bool, jsii.invoke(self, "mutateRemoveLink", [link]))

    @jsii.member(jsii_name="mutateRemoveReverseLink")
    def mutate_remove_reverse_link(self, link: Edge) -> builtins.bool:
        '''(experimental) Remove a *link* to *this node*.

        :param link: -

        :stability: experimental
        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcc8ef830bc8b60569c5d33ea798ceb1607d531edba6cb7907677008c0fffbdb)
            check_type(argname="argument link", value=link, expected_type=type_hints["link"])
        return typing.cast(builtins.bool, jsii.invoke(self, "mutateRemoveReverseLink", [link]))

    @jsii.member(jsii_name="mutateUncluster")
    def mutate_uncluster(self) -> None:
        '''(experimental) Hoist all children to parent and collapse node to parent.

        :stability: experimental
        :destructive: true
        '''
        return typing.cast(None, jsii.invoke(self, "mutateUncluster", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Get string representation of this node.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="allowDestructiveMutations")
    def allow_destructive_mutations(self) -> builtins.bool:
        '''(experimental) Indicates if this node allows destructive mutations.

        :see: {@link Store.allowDestructiveMutations }
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "allowDestructiveMutations"))

    @builtins.property
    @jsii.member(jsii_name="children")
    def children(self) -> typing.List["Node"]:
        '''(experimental) Get all direct child nodes.

        :stability: experimental
        '''
        return typing.cast(typing.List["Node"], jsii.get(self, "children"))

    @builtins.property
    @jsii.member(jsii_name="dependedOnBy")
    def depended_on_by(self) -> typing.List["Node"]:
        '''(experimental) Get list of **Nodes** that *depend on this node*.

        :see: {@link Node.reverseDependencyLinks }
        :stability: experimental
        '''
        return typing.cast(typing.List["Node"], jsii.get(self, "dependedOnBy"))

    @builtins.property
    @jsii.member(jsii_name="dependencies")
    def dependencies(self) -> typing.List["Node"]:
        '''(experimental) Get list of **Nodes** that *this node depends on*.

        :see: {@link Node.dependencyLinks }
        :stability: experimental
        '''
        return typing.cast(typing.List["Node"], jsii.get(self, "dependencies"))

    @builtins.property
    @jsii.member(jsii_name="dependencyLinks")
    def dependency_links(self) -> typing.List["Dependency"]:
        '''(experimental) Gets list of {@link Dependency} links (edges) where this node is the **source**.

        :stability: experimental
        '''
        return typing.cast(typing.List["Dependency"], jsii.get(self, "dependencyLinks"))

    @builtins.property
    @jsii.member(jsii_name="depth")
    def depth(self) -> jsii.Number:
        '''(experimental) Indicates the depth of the node relative to root (0).

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "depth"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''(experimental) Node id, which is only unique within parent scope.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="isAsset")
    def is_asset(self) -> builtins.bool:
        '''(experimental) Indicates if this node is considered a {@link FlagEnum.ASSET}.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isAsset"))

    @builtins.property
    @jsii.member(jsii_name="isCfnFqn")
    def is_cfn_fqn(self) -> builtins.bool:
        '''(experimental) Indicates if node ConstructInfoFqn denotes a ``aws-cdk-lib.*.Cfn*`` construct.

        :see: {@link FlagEnum.CFN_FQN }
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isCfnFqn"))

    @builtins.property
    @jsii.member(jsii_name="isCluster")
    def is_cluster(self) -> builtins.bool:
        '''(experimental) Indicates if this node is considered a {@link FlagEnum.CLUSTER}.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isCluster"))

    @builtins.property
    @jsii.member(jsii_name="isCustomResource")
    def is_custom_resource(self) -> builtins.bool:
        '''(experimental) Indicates if node is a *Custom Resource*.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isCustomResource"))

    @builtins.property
    @jsii.member(jsii_name="isExtraneous")
    def is_extraneous(self) -> builtins.bool:
        '''(experimental) Indicates if this node is considered a {@link FlagEnum.EXTRANEOUS} node or determined to be extraneous: - Clusters that contain no children.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isExtraneous"))

    @builtins.property
    @jsii.member(jsii_name="isGraphContainer")
    def is_graph_container(self) -> builtins.bool:
        '''(experimental) Indicates if this node is considered a {@link FlagEnum.GRAPH_CONTAINER}.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isGraphContainer"))

    @builtins.property
    @jsii.member(jsii_name="isLeaf")
    def is_leaf(self) -> builtins.bool:
        '''(experimental) Indicates if this node is a *leaf* node, which means it does not have children.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isLeaf"))

    @builtins.property
    @jsii.member(jsii_name="isTopLevel")
    def is_top_level(self) -> builtins.bool:
        '''(experimental) Indicates if node is direct child of the graph root node.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isTopLevel"))

    @builtins.property
    @jsii.member(jsii_name="links")
    def links(self) -> typing.List[Edge]:
        '''(experimental) Gets all links (edges) in which this node is the **source**.

        :stability: experimental
        '''
        return typing.cast(typing.List[Edge], jsii.get(self, "links"))

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> NodeTypeEnum:
        '''(experimental) Type of node.

        :stability: experimental
        '''
        return typing.cast(NodeTypeEnum, jsii.get(self, "nodeType"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        '''(experimental) Path of the node.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="referencedBy")
    def referenced_by(self) -> typing.List["Node"]:
        '''(experimental) Get list of **Nodes** that *reference this node*.

        :see: {@link Node.reverseReferenceLinks }
        :stability: experimental
        '''
        return typing.cast(typing.List["Node"], jsii.get(self, "referencedBy"))

    @builtins.property
    @jsii.member(jsii_name="referenceLinks")
    def reference_links(self) -> typing.List["Reference"]:
        '''(experimental) Gets list of {@link Reference} links (edges) where this node is the **source**.

        :stability: experimental
        '''
        return typing.cast(typing.List["Reference"], jsii.get(self, "referenceLinks"))

    @builtins.property
    @jsii.member(jsii_name="references")
    def references(self) -> typing.List["Node"]:
        '''(experimental) Get list of **Nodes** that *this node references*.

        :see: {@link Node.referenceLinks }
        :stability: experimental
        '''
        return typing.cast(typing.List["Node"], jsii.get(self, "references"))

    @builtins.property
    @jsii.member(jsii_name="reverseDependencyLinks")
    def reverse_dependency_links(self) -> typing.List["Dependency"]:
        '''(experimental) Gets list of {@link Dependency} links (edges) where this node is the **target**.

        :stability: experimental
        '''
        return typing.cast(typing.List["Dependency"], jsii.get(self, "reverseDependencyLinks"))

    @builtins.property
    @jsii.member(jsii_name="reverseLinks")
    def reverse_links(self) -> typing.List[Edge]:
        '''(experimental) Gets all links (edges) in which this node is the **target**.

        :stability: experimental
        '''
        return typing.cast(typing.List[Edge], jsii.get(self, "reverseLinks"))

    @builtins.property
    @jsii.member(jsii_name="reverseReferenceLinks")
    def reverse_reference_links(self) -> typing.List["Reference"]:
        '''(experimental) Gets list of {@link Reference} links (edges) where this node is the **target**.

        :stability: experimental
        '''
        return typing.cast(typing.List["Reference"], jsii.get(self, "reverseReferenceLinks"))

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List["Node"]:
        '''(experimental) Gets descending ordered list of ancestors from the root.

        :stability: experimental
        '''
        return typing.cast(typing.List["Node"], jsii.get(self, "scopes"))

    @builtins.property
    @jsii.member(jsii_name="siblings")
    def siblings(self) -> typing.List["Node"]:
        '''(experimental) Get list of *siblings* of this node.

        :stability: experimental
        '''
        return typing.cast(typing.List["Node"], jsii.get(self, "siblings"))

    @builtins.property
    @jsii.member(jsii_name="cfnProps")
    def cfn_props(self) -> typing.Optional[PlainObject]:
        '''(experimental) Gets CloudFormation properties for this node.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[PlainObject], jsii.get(self, "cfnProps"))

    @builtins.property
    @jsii.member(jsii_name="cfnType")
    def cfn_type(self) -> typing.Optional[builtins.str]:
        '''(experimental) Get the CloudFormation resource type for this node.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cfnType"))

    @builtins.property
    @jsii.member(jsii_name="constructInfo")
    def construct_info(self) -> typing.Optional[ConstructInfo]:
        '''(experimental) Synthesized construct information defining jii resolution data.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[ConstructInfo], jsii.get(self, "constructInfo"))

    @builtins.property
    @jsii.member(jsii_name="constructInfoFqn")
    def construct_info_fqn(self) -> typing.Optional[builtins.str]:
        '''(experimental) Synthesized construct information defining jii resolution data.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "constructInfoFqn"))

    @builtins.property
    @jsii.member(jsii_name="logicalId")
    def logical_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) Logical id of the node, which is only unique within containing stack.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logicalId"))

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> typing.Optional["Node"]:
        '''(experimental) Parent node.

        Only the root node should not have parent.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["Node"], jsii.get(self, "parent"))

    @builtins.property
    @jsii.member(jsii_name="rootStack")
    def root_stack(self) -> typing.Optional["StackNode"]:
        '''(experimental) Get **root** stack.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["StackNode"], jsii.get(self, "rootStack"))

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> typing.Optional["StackNode"]:
        '''(experimental) Stack the node is contained in.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["StackNode"], jsii.get(self, "stack"))


class OutputNode(
    Node,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-prototyping-sdk/cdk-graph.OutputNode",
):
    '''(experimental) OutputNode defines a cdk CfnOutput resources.

    :stability: experimental
    '''

    def __init__(self, props: IOutputNodeProps) -> None:
        '''
        :param props: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3da145a8289db66b0d336f3e315bdf68451e5f68af71ee47e03d07f6e5c4a4a4)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isOutputNode")
    @builtins.classmethod
    def is_output_node(cls, node: Node) -> builtins.bool:
        '''(experimental) Indicates if node is an {@link OutputNode}.

        :param node: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a127ae0d40eecf96bdf403e311388722667e462513fbf566c60d8e6f58539cfa)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isOutputNode", [node]))

    @jsii.member(jsii_name="mutateDestroy")
    def mutate_destroy(self, strict: typing.Optional[builtins.bool] = None) -> None:
        '''(experimental) Destroys this node by removing all references and removing this node from the store.

        :param strict: -

        :stability: experimental
        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e55e96ec84c6585331429d9addc5c1ebf5414133101eb4528626f9042720eb4f)
            check_type(argname="argument strict", value=strict, expected_type=type_hints["strict"])
        return typing.cast(None, jsii.invoke(self, "mutateDestroy", [strict]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ATTR_EXPORT_NAME")
    def ATTR_EXPORT_NAME(cls) -> builtins.str:
        '''(experimental) Attribute key where output export name is stored.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ATTR_EXPORT_NAME"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ATTR_VALUE")
    def ATTR_VALUE(cls) -> builtins.str:
        '''(experimental) Attribute key where output value is stored.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ATTR_VALUE"))

    @builtins.property
    @jsii.member(jsii_name="isExport")
    def is_export(self) -> builtins.bool:
        '''(experimental) Indicates if {@link OutputNode} is **exported**.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isExport"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Any:
        '''(experimental) Get the *value** attribute.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="exportName")
    def export_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Get the export name attribute.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exportName"))


class ParameterNode(
    Node,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-prototyping-sdk/cdk-graph.ParameterNode",
):
    '''(experimental) ParameterNode defines a CfnParameter node.

    :stability: experimental
    '''

    def __init__(self, props: IParameterNodeProps) -> None:
        '''
        :param props: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6bad65a471e15f8ee779034629700c50cdf0c04cb7d2dcd091132895e2aa49f)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isParameterNode")
    @builtins.classmethod
    def is_parameter_node(cls, node: Node) -> builtins.bool:
        '''(experimental) Indicates if node is a {@link ParameterNode}.

        :param node: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__621af1c40617acac1c635f63f857e3dfdbe754e7f7f5ac44edc794f02cc8aa62)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isParameterNode", [node]))

    @jsii.member(jsii_name="mutateDestroy")
    def mutate_destroy(self, strict: typing.Optional[builtins.bool] = None) -> None:
        '''(experimental) Destroys this node by removing all references and removing this node from the store.

        :param strict: -

        :stability: experimental
        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc8f87ea7f23941a2ade0f5147d5a9c62e340781cc71ac5a027cbeb1f90f8760)
            check_type(argname="argument strict", value=strict, expected_type=type_hints["strict"])
        return typing.cast(None, jsii.invoke(self, "mutateDestroy", [strict]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ATTR_TYPE")
    def ATTR_TYPE(cls) -> builtins.str:
        '''(experimental) Attribute key where parameter type is stored.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ATTR_TYPE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ATTR_VALUE")
    def ATTR_VALUE(cls) -> builtins.str:
        '''(experimental) Attribute key where parameter value is store.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ATTR_VALUE"))

    @builtins.property
    @jsii.member(jsii_name="isStackReference")
    def is_stack_reference(self) -> builtins.bool:
        '''(experimental) Indicates if parameter is a reference to a stack.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isStackReference"))

    @builtins.property
    @jsii.member(jsii_name="parameterType")
    def parameter_type(self) -> typing.Any:
        '''(experimental) Get the parameter type attribute.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.get(self, "parameterType"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Any:
        '''(experimental) Get the value attribute.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.get(self, "value"))


class Reference(
    Edge,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-prototyping-sdk/cdk-graph.Reference",
):
    '''(experimental) Reference edge class defines a directed relationship between nodes.

    :stability: experimental
    '''

    def __init__(self, props: IReferenceProps) -> None:
        '''
        :param props: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13cbf6dec7094f31d6fc6f739bbf44b5b4b63d0b0a6b3862a1a164c86b374cde)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isRef")
    @builtins.classmethod
    def is_ref(cls, edge: Edge) -> builtins.bool:
        '''(experimental) Indicates if edge is a **Ref** based {@link Reference} edge.

        :param edge: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdce1dd0ab4d7b2d805c4d9711b42f8cdb82da30805f659d176efe9f34594d2d)
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isRef", [edge]))

    @jsii.member(jsii_name="isReference")
    @builtins.classmethod
    def is_reference(cls, edge: Edge) -> builtins.bool:
        '''(experimental) Indicates if edge is a {@link Reference}.

        :param edge: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8c12e3117f04b4e98b681272a904b6082dce26884c1976de71fdba4e42603f7)
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isReference", [edge]))

    @jsii.member(jsii_name="resolveChain")
    def resolve_chain(self) -> typing.List[typing.Any]:
        '''(experimental) Resolve reference chain.

        :stability: experimental
        '''
        return typing.cast(typing.List[typing.Any], jsii.invoke(self, "resolveChain", []))

    @jsii.member(jsii_name="resolveTargets")
    def resolve_targets(self) -> typing.List[Node]:
        '''(experimental) Resolve targets by following potential edge chain.

        :see: {@link EdgeChain }
        :stability: experimental
        '''
        return typing.cast(typing.List[Node], jsii.invoke(self, "resolveTargets", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ATT_TYPE")
    def ATT_TYPE(cls) -> builtins.str:
        '''(experimental) Attribute defining the type of reference.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ATT_TYPE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PREFIX")
    def PREFIX(cls) -> builtins.str:
        '''(experimental) Edge prefix to denote **Ref** type reference edge.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PREFIX"))

    @builtins.property
    @jsii.member(jsii_name="referenceType")
    def reference_type(self) -> ReferenceTypeEnum:
        '''(experimental) Get type of reference.

        :stability: experimental
        '''
        return typing.cast(ReferenceTypeEnum, jsii.get(self, "referenceType"))


class ResourceNode(
    Node,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-prototyping-sdk/cdk-graph.ResourceNode",
):
    '''(experimental) ResourceNode class defines a L2 cdk resource construct.

    :stability: experimental
    '''

    def __init__(self, props: IResourceNodeProps) -> None:
        '''
        :param props: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c6c9f4ced42ead844dc1054e31bd1b78f4e8e0d0b252cb49ab29ea9a39ea70b)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isResourceNode")
    @builtins.classmethod
    def is_resource_node(cls, node: Node) -> builtins.bool:
        '''(experimental) Indicates if node is a {@link ResourceNode}.

        :param node: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0453f99caba49f66a98152ee3485b1bf8866146a898149773967a2c0bc2f6dac)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isResourceNode", [node]))

    @jsii.member(jsii_name="mutateCfnResource")
    def mutate_cfn_resource(
        self,
        cfn_resource: typing.Optional["CfnResourceNode"] = None,
    ) -> None:
        '''(experimental) Modifies the L1 resource wrapped by this L2 resource.

        :param cfn_resource: -

        :stability: experimental
        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f0870fe328fea4963f5221f2a3c0f0496fe542e20c7804c93866e881daec5d4)
            check_type(argname="argument cfn_resource", value=cfn_resource, expected_type=type_hints["cfn_resource"])
        return typing.cast(None, jsii.invoke(self, "mutateCfnResource", [cfn_resource]))

    @jsii.member(jsii_name="mutateRemoveChild")
    def mutate_remove_child(self, node: Node) -> builtins.bool:
        '''(experimental) Remove a *child* node from *this node*.

        :param node: -

        :stability: experimental
        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31ffb4369b94961c7784bf8d2b3fe8b642d68211d9339037a9aa3f8672ea96c3)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.invoke(self, "mutateRemoveChild", [node]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ATT_WRAPPED_CFN_PROPS")
    def ATT_WRAPPED_CFN_PROPS(cls) -> builtins.str:
        '''(experimental) Attribute key for cfn properties.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ATT_WRAPPED_CFN_PROPS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ATT_WRAPPED_CFN_TYPE")
    def ATT_WRAPPED_CFN_TYPE(cls) -> builtins.str:
        '''(experimental) Attribute key for cfn resource type.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ATT_WRAPPED_CFN_TYPE"))

    @builtins.property
    @jsii.member(jsii_name="isCdkOwned")
    def is_cdk_owned(self) -> builtins.bool:
        '''(experimental) Indicates if this resource is owned by cdk (defined in cdk library).

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isCdkOwned"))

    @builtins.property
    @jsii.member(jsii_name="isWrapper")
    def is_wrapper(self) -> builtins.bool:
        '''(experimental) Indicates if Resource wraps a single CfnResource.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isWrapper"))

    @builtins.property
    @jsii.member(jsii_name="cfnProps")
    def cfn_props(self) -> typing.Optional[PlainObject]:
        '''(experimental) Get the cfn properties from the L1 resource that this L2 resource wraps.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[PlainObject], jsii.get(self, "cfnProps"))

    @builtins.property
    @jsii.member(jsii_name="cfnResource")
    def cfn_resource(self) -> typing.Optional["CfnResourceNode"]:
        '''(experimental) Get the default/primary CfnResource that this Resource wraps.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["CfnResourceNode"], jsii.get(self, "cfnResource"))

    @builtins.property
    @jsii.member(jsii_name="cfnType")
    def cfn_type(self) -> typing.Optional[builtins.str]:
        '''(experimental) Get the CloudFormation resource type for this L2 resource or for the L1 resource is wraps.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cfnType"))


class RootNode(
    Node,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-prototyping-sdk/cdk-graph.RootNode",
):
    '''(experimental) RootNode represents the root of the store tree.

    :stability: experimental
    '''

    def __init__(self, store: Store) -> None:
        '''
        :param store: Reference to the store.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2858e1c353684c85393980ddd8171e738a810cdb39195bdd4b1fc5a5129877f4)
            check_type(argname="argument store", value=store, expected_type=type_hints["store"])
        jsii.create(self.__class__, self, [store])

    @jsii.member(jsii_name="isRootNode")
    @builtins.classmethod
    def is_root_node(cls, node: Node) -> builtins.bool:
        '''(experimental) Indicates if node is a {@link RootNode}.

        :param node: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a94129a7134d7f30f6f7df7c59273964794f931bc432072d1d3cdafed475f2d)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isRootNode", [node]))

    @jsii.member(jsii_name="findAll")
    def find_all(
        self,
        options: typing.Optional[IFindNodeOptions] = None,
    ) -> typing.List[Node]:
        '''(experimental) Return this construct and all of its sub-nodes in the given order.

        Optionally filter nodes based on predicate.
        **The root not is excluded from list**

        :param options: -

        :stability: experimental
        :inheritdoc: **The root not is excluded from list**
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52135bc8e4aa332f0c9ae263f6b1f3b0171e5b60a962c50cda9981f7cd12b769)
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
        return typing.cast(typing.List[Node], jsii.invoke(self, "findAll", [options]))

    @jsii.member(jsii_name="mutateCollapse")
    def mutate_collapse(self) -> None:
        '''(experimental) Collapses all sub-nodes of *this node* into *this node*.

        .. epigraph::

           {@link RootNode} does not support this mutation

        :stability: experimental
        :inheritdoc: true
        :throws: Error does not support
        '''
        return typing.cast(None, jsii.invoke(self, "mutateCollapse", []))

    @jsii.member(jsii_name="mutateCollapseTo")
    def mutate_collapse_to(self, _ancestor: Node) -> Node:
        '''(experimental) Collapses *this node* into *an ancestor* > {@link RootNode} does not support this mutation.

        :param _ancestor: -

        :stability: experimental
        :inheritdoc: true
        :throws: Error does not support
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70cddb7519cff2871f863c6cd3e0249639b48424c7127867dba034a8dcb68e1f)
            check_type(argname="argument _ancestor", value=_ancestor, expected_type=type_hints["_ancestor"])
        return typing.cast(Node, jsii.invoke(self, "mutateCollapseTo", [_ancestor]))

    @jsii.member(jsii_name="mutateCollapseToParent")
    def mutate_collapse_to_parent(self) -> Node:
        '''(experimental) Collapses *this node* into *it's parent node* > {@link RootNode} does not support this mutation.

        :stability: experimental
        :inheritdoc: true
        :throws: Error does not support
        '''
        return typing.cast(Node, jsii.invoke(self, "mutateCollapseToParent", []))

    @jsii.member(jsii_name="mutateDestroy")
    def mutate_destroy(self, _strict: typing.Optional[builtins.bool] = None) -> None:
        '''(experimental) Destroys this node by removing all references and removing this node from the store.

        .. epigraph::

           {@link RootNode} does not support this mutation

        :param _strict: -

        :stability: experimental
        :inheritdoc: true
        :throws: Error does not support
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de6bbc2b0a38053065cef3efa2294d4187e740588afc3ded564fc359f94245c2)
            check_type(argname="argument _strict", value=_strict, expected_type=type_hints["_strict"])
        return typing.cast(None, jsii.invoke(self, "mutateDestroy", [_strict]))

    @jsii.member(jsii_name="mutateHoist")
    def mutate_hoist(self, _new_parent: Node) -> None:
        '''(experimental) Hoist *this node* to an *ancestor* by removing it from its current parent node and in turn moving it to the ancestor.

        .. epigraph::

           {@link RootNode} does not support this mutation

        :param _new_parent: -

        :stability: experimental
        :inheritdoc: true
        :throws: Error does not support
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d4a7bad4f9d7ba1fd95de784e042abc8d2fca9c2352f2626b664afd09d1652f)
            check_type(argname="argument _new_parent", value=_new_parent, expected_type=type_hints["_new_parent"])
        return typing.cast(None, jsii.invoke(self, "mutateHoist", [_new_parent]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PATH")
    def PATH(cls) -> builtins.str:
        '''(experimental) Fixed path of root.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PATH"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="UUID")
    def UUID(cls) -> builtins.str:
        '''(experimental) Fixed UUID of root.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "UUID"))


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/cdk-graph.SGEdge",
    jsii_struct_bases=[SGEntity],
    name_mapping={
        "uuid": "uuid",
        "attributes": "attributes",
        "flags": "flags",
        "metadata": "metadata",
        "tags": "tags",
        "direction": "direction",
        "edge_type": "edgeType",
        "source": "source",
        "target": "target",
    },
)
class SGEdge(SGEntity):
    def __init__(
        self,
        *,
        uuid: builtins.str,
        attributes: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]]]]]]] = None,
        flags: typing.Optional[typing.Sequence[FlagEnum]] = None,
        metadata: typing.Optional[typing.Sequence[typing.Union[_constructs_77d1e7e8.MetadataEntry, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        direction: EdgeDirectionEnum,
        edge_type: EdgeTypeEnum,
        source: builtins.str,
        target: builtins.str,
    ) -> None:
        '''(experimental) Serializable graph edge entity.

        :param uuid: (experimental) Universally unique identity.
        :param attributes: (experimental) Serializable entity attributes.
        :param flags: (experimental) Serializable entity flags.
        :param metadata: (experimental) Serializable entity metadata.
        :param tags: (experimental) Serializable entity tags.
        :param direction: (experimental) Indicates the direction in which the edge is directed.
        :param edge_type: (experimental) Type of edge.
        :param source: (experimental) UUID of edge **source** node (tail).
        :param target: (experimental) UUID of edge **target** node (head).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e6e44c6ff3c944799ca44f751aee392acaa420b9a44b401db722bf60be6a51e)
            check_type(argname="argument uuid", value=uuid, expected_type=type_hints["uuid"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument flags", value=flags, expected_type=type_hints["flags"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument direction", value=direction, expected_type=type_hints["direction"])
            check_type(argname="argument edge_type", value=edge_type, expected_type=type_hints["edge_type"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uuid": uuid,
            "direction": direction,
            "edge_type": edge_type,
            "source": source,
            "target": target,
        }
        if attributes is not None:
            self._values["attributes"] = attributes
        if flags is not None:
            self._values["flags"] = flags
        if metadata is not None:
            self._values["metadata"] = metadata
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def uuid(self) -> builtins.str:
        '''(experimental) Universally unique identity.

        :stability: experimental
        '''
        result = self._values.get("uuid")
        assert result is not None, "Required property 'uuid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]]]:
        '''(experimental) Serializable entity attributes.

        :see: {@link Attributes }
        :stability: experimental
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]]], result)

    @builtins.property
    def flags(self) -> typing.Optional[typing.List[FlagEnum]]:
        '''(experimental) Serializable entity flags.

        :see: {@link FlagEnum }
        :stability: experimental
        '''
        result = self._values.get("flags")
        return typing.cast(typing.Optional[typing.List[FlagEnum]], result)

    @builtins.property
    def metadata(
        self,
    ) -> typing.Optional[typing.List[_constructs_77d1e7e8.MetadataEntry]]:
        '''(experimental) Serializable entity metadata.

        :see: {@link Metadata }
        :stability: experimental
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.List[_constructs_77d1e7e8.MetadataEntry]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Serializable entity tags.

        :see: {@link Tags }
        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def direction(self) -> EdgeDirectionEnum:
        '''(experimental) Indicates the direction in which the edge is directed.

        :stability: experimental
        '''
        result = self._values.get("direction")
        assert result is not None, "Required property 'direction' is missing"
        return typing.cast(EdgeDirectionEnum, result)

    @builtins.property
    def edge_type(self) -> EdgeTypeEnum:
        '''(experimental) Type of edge.

        :stability: experimental
        '''
        result = self._values.get("edge_type")
        assert result is not None, "Required property 'edge_type' is missing"
        return typing.cast(EdgeTypeEnum, result)

    @builtins.property
    def source(self) -> builtins.str:
        '''(experimental) UUID of edge **source**  node (tail).

        :stability: experimental
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> builtins.str:
        '''(experimental) UUID of edge **target**  node (head).

        :stability: experimental
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SGEdge(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StackNode(
    Node,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-prototyping-sdk/cdk-graph.StackNode",
):
    '''(experimental) StackNode defines a cdk Stack.

    :stability: experimental
    '''

    def __init__(self, props: IStackNodeProps) -> None:
        '''
        :param props: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c406dbfcbf0e87f9fb3c3b858a4c75940a4979183139c582777ed42545ffc8d)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isStackNode")
    @builtins.classmethod
    def is_stack_node(cls, node: Node) -> builtins.bool:
        '''(experimental) Indicates if node is a {@link StackNode}.

        :param node: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c115a0983440348d31ae427389290c8619bdbc92e3c99929796ed50695aa950f)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isStackNode", [node]))

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, node: Node) -> "StackNode":
        '''(experimental) Gets the {@link StackNode} containing a given resource.

        :param node: -

        :stability: experimental
        :throws: Error is node is not contained in a stack
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__915f11470d516a7f8701600fa93eff5ba4671cdccd560f50667a796863bec880)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast("StackNode", jsii.sinvoke(cls, "of", [node]))

    @jsii.member(jsii_name="addOutput")
    def add_output(self, node: OutputNode) -> None:
        '''(experimental) Associate {@link OutputNode} with this stack.

        :param node: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49ca515fbc945e2ec37d58c6ce8e826d049ebedbdb7a9ad6e414502e213b1ca5)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "addOutput", [node]))

    @jsii.member(jsii_name="addParameter")
    def add_parameter(self, node: ParameterNode) -> None:
        '''(experimental) Associate {@link ParameterNode} with this stack.

        :param node: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03facf341abc9ea1d0cc8d187a70c5a1eecdc35758cc5c772206af6629d5a3d1)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "addParameter", [node]))

    @jsii.member(jsii_name="findOutput")
    def find_output(self, logical_id: builtins.str) -> OutputNode:
        '''(experimental) Find {@link OutputNode} with *logicalId* defined by this stack.

        :param logical_id: -

        :stability: experimental
        :throws: Error is no output found matching *logicalId*
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1a6a8c26e687161d550aa54c20c52e9ce74e768edb15bffb12e2c5d7cd35ebc)
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
        return typing.cast(OutputNode, jsii.invoke(self, "findOutput", [logical_id]))

    @jsii.member(jsii_name="findParameter")
    def find_parameter(self, parameter_id: builtins.str) -> ParameterNode:
        '''(experimental) Find {@link ParameterNode} with *parameterId* defined by this stack.

        :param parameter_id: -

        :stability: experimental
        :throws: Error is no parameter found matching *parameterId*
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33dc300f7e88e048c333d0f73c36a0cb5650500af888901a74cdca29eaa5f47b)
            check_type(argname="argument parameter_id", value=parameter_id, expected_type=type_hints["parameter_id"])
        return typing.cast(ParameterNode, jsii.invoke(self, "findParameter", [parameter_id]))

    @jsii.member(jsii_name="mutateDestroy")
    def mutate_destroy(self, strict: typing.Optional[builtins.bool] = None) -> None:
        '''(experimental) Destroys this node by removing all references and removing this node from the store.

        :param strict: -

        :stability: experimental
        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4728fd8b6c5b6dad937d4d5029f42a9d43d95d2bb8fa97c5dd6c0a831fc0e5cc)
            check_type(argname="argument strict", value=strict, expected_type=type_hints["strict"])
        return typing.cast(None, jsii.invoke(self, "mutateDestroy", [strict]))

    @jsii.member(jsii_name="mutateHoist")
    def mutate_hoist(self, new_parent: Node) -> None:
        '''(experimental) Hoist *this node* to an *ancestor* by removing it from its current parent node and in turn moving it to the ancestor.

        :param new_parent: -

        :stability: experimental
        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb94dd9f583fcaea84f5de0db1cd5e8dfce57b1e8c54483769c4dc8e97687fb2)
            check_type(argname="argument new_parent", value=new_parent, expected_type=type_hints["new_parent"])
        return typing.cast(None, jsii.invoke(self, "mutateHoist", [new_parent]))

    @jsii.member(jsii_name="mutateRemoveOutput")
    def mutate_remove_output(self, node: OutputNode) -> builtins.bool:
        '''(experimental) Disassociate {@link OutputNode} from this stack.

        :param node: -

        :stability: experimental
        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21c7e2103930b4528e19756f0d2147608cc076167cd22be28f088c7faf602d3a)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.invoke(self, "mutateRemoveOutput", [node]))

    @jsii.member(jsii_name="mutateRemoveParameter")
    def mutate_remove_parameter(self, node: ParameterNode) -> builtins.bool:
        '''(experimental) Disassociate {@link ParameterNode} from this stack.

        :param node: -

        :stability: experimental
        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77dcc17a3ce0b81b743d5659ee012e356bdcc6bc70eef717249ef76b3bfe64a0)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.invoke(self, "mutateRemoveParameter", [node]))

    @builtins.property
    @jsii.member(jsii_name="exports")
    def exports(self) -> typing.List[OutputNode]:
        '''(experimental) Get all **exported** {@link OutputNode}s defined by this stack.

        :stability: experimental
        '''
        return typing.cast(typing.List[OutputNode], jsii.get(self, "exports"))

    @builtins.property
    @jsii.member(jsii_name="outputs")
    def outputs(self) -> typing.List[OutputNode]:
        '''(experimental) Get all {@link OutputNode}s defined by this stack.

        :stability: experimental
        '''
        return typing.cast(typing.List[OutputNode], jsii.get(self, "outputs"))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.List[ParameterNode]:
        '''(experimental) Get all {@link ParameterNode}s defined by this stack.

        :stability: experimental
        '''
        return typing.cast(typing.List[ParameterNode], jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="stage")
    def stage(self) -> typing.Optional["StageNode"]:
        '''(experimental) Get {@link StageNode} containing this stack.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["StageNode"], jsii.get(self, "stage"))


class StageNode(
    Node,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-prototyping-sdk/cdk-graph.StageNode",
):
    '''(experimental) StageNode defines a cdk Stage.

    :stability: experimental
    '''

    def __init__(self, props: ITypedNodeProps) -> None:
        '''
        :param props: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcaf74ca37e625ffeed9d5a60c5941b594c1d056c261a203d0ff7aae64286f1f)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isStageNode")
    @builtins.classmethod
    def is_stage_node(cls, node: Node) -> builtins.bool:
        '''(experimental) Indicates if node is a {@link StageNode}.

        :param node: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeb6a55a082be98aa517799c51da665a5caae79ff73869e9bd2c23b62e8651ed)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isStageNode", [node]))

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, node: Node) -> "StageNode":
        '''(experimental) Gets the {@link StageNode} containing a given resource.

        :param node: -

        :stability: experimental
        :throws: Error is node is not contained in a stage
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c264d84efa90db43f239ad81dcb04b7271c5e764e17e01b895d86f1dca6bcd2)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast("StageNode", jsii.sinvoke(cls, "of", [node]))

    @jsii.member(jsii_name="addStack")
    def add_stack(self, stack: StackNode) -> None:
        '''(experimental) Associate a {@link StackNode} with this stage.

        :param stack: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeb1552ad75e63308b0fecbac20851396abc4f79f77267a45c3661a9920b0360)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        return typing.cast(None, jsii.invoke(self, "addStack", [stack]))

    @jsii.member(jsii_name="mutateRemoveStack")
    def mutate_remove_stack(self, stack: StackNode) -> builtins.bool:
        '''(experimental) Disassociate {@link StackNode} from this stage.

        :param stack: -

        :stability: experimental
        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17fef2232e4c6702e399a03209088941244a15f0663c7fdc456a9386c4035036)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        return typing.cast(builtins.bool, jsii.invoke(self, "mutateRemoveStack", [stack]))

    @builtins.property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> typing.List[StackNode]:
        '''(experimental) Gets all stacks contained by this stage.

        :stability: experimental
        '''
        return typing.cast(typing.List[StackNode], jsii.get(self, "stacks"))


class AppNode(
    Node,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-prototyping-sdk/cdk-graph.AppNode",
):
    '''(experimental) AppNode defines a cdk App.

    :stability: experimental
    '''

    def __init__(self, props: IAppNodeProps) -> None:
        '''
        :param props: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b54478d4eff82d80f3fa3c12926f6c1eb7d1cbbba5cf0d54104c45ba8d2932da)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isAppNode")
    @builtins.classmethod
    def is_app_node(cls, node: Node) -> builtins.bool:
        '''(experimental) Indicates if node is a {@link AppNode}.

        :param node: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__337b277c4153037ed28c9def7def7aad44b9178fbe02bc5babf708d344a92c26)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isAppNode", [node]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PATH")
    def PATH(cls) -> builtins.str:
        '''(experimental) Fixed path of the App.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PATH"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="UUID")
    def UUID(cls) -> builtins.str:
        '''(experimental) Fixed UUID for App node.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "UUID"))


class AttributeReference(
    Reference,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-prototyping-sdk/cdk-graph.AttributeReference",
):
    '''(experimental) Attribute type reference edge.

    :stability: experimental
    '''

    def __init__(self, props: IAttributeReferenceProps) -> None:
        '''
        :param props: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0563f317c98960c719cf66869e770302bcc324f313aee0ef635224e07ce1e633)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isAtt")
    @builtins.classmethod
    def is_att(cls, edge: Edge) -> builtins.bool:
        '''(experimental) Indicates if edge in an **Fn::GetAtt** {@link Reference}.

        :param edge: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dac13a68a078eda02db5a11164b8f3e3c55dc0dbabb4ec1d988c11b8a2a6310)
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isAtt", [edge]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ATT_VALUE")
    def ATT_VALUE(cls) -> builtins.str:
        '''(experimental) Attribute key for resolved value of attribute reference.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ATT_VALUE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PREFIX")
    def PREFIX(cls) -> builtins.str:
        '''(experimental) Edge prefix to denote **Fn::GetAtt** type reference edge.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PREFIX"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        '''(experimental) Get the resolved attribute value.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "value"))


class CfnResourceNode(
    Node,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-prototyping-sdk/cdk-graph.CfnResourceNode",
):
    '''(experimental) CfnResourceNode defines an L1 cdk resource.

    :stability: experimental
    '''

    def __init__(self, props: ICfnResourceNodeProps) -> None:
        '''
        :param props: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__475b66da39f8ade9b8105ab8da9507c2cee4dfaea064d6e21a560fcb4a77214a)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isCfnResourceNode")
    @builtins.classmethod
    def is_cfn_resource_node(cls, node: Node) -> builtins.bool:
        '''(experimental) Indicates if a node is a {@link CfnResourceNode}.

        :param node: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2c3aed894ebb341f41635244c6a2f64947719e15b0cc56970b21706635d9a9b)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnResourceNode", [node]))

    @jsii.member(jsii_name="isEquivalentFqn")
    def is_equivalent_fqn(self, resource: ResourceNode) -> builtins.bool:
        '''(experimental) Evaluates if CfnResourceNode fqn is equivalent to ResourceNode fqn.

        :param resource: - {@link Graph.ResourceNode } to compare.

        :return: Returns ``true`` if equivalent, otherwise ``false``

        :stability: experimental

        Example::

            `aws-cdk-lib.aws_lambda.Function` => `aws-cdk-lib.aws_lambda.CfnFunction`
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__374ac098fdc910e98fa76178b8f501b519407c242f829d1e95e81c1d11096047)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.bool, jsii.invoke(self, "isEquivalentFqn", [resource]))

    @jsii.member(jsii_name="mutateDestroy")
    def mutate_destroy(self, strict: typing.Optional[builtins.bool] = None) -> None:
        '''(experimental) Destroys this node by removing all references and removing this node from the store.

        :param strict: -

        :stability: experimental
        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d5a2459368e54cc121bca01b26d4f7b45053e99925670e317a889e82b943cca)
            check_type(argname="argument strict", value=strict, expected_type=type_hints["strict"])
        return typing.cast(None, jsii.invoke(self, "mutateDestroy", [strict]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ATT_IMPORT_ARN_TOKEN")
    def ATT_IMPORT_ARN_TOKEN(cls) -> builtins.str:
        '''(experimental) Normalized CfnReference attribute.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ATT_IMPORT_ARN_TOKEN"))

    @builtins.property
    @jsii.member(jsii_name="isExtraneous")
    def is_extraneous(self) -> builtins.bool:
        '''(experimental) Indicates if this node is considered a {@link FlagEnum.EXTRANEOUS} node or determined to be extraneous: - Clusters that contain no children.

        :stability: experimental
        :inheritdoc: true
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isExtraneous"))

    @builtins.property
    @jsii.member(jsii_name="isImport")
    def is_import(self) -> builtins.bool:
        '''(experimental) Indicates if this CfnResource is imported (eg: ``s3.Bucket.fromBucketArn``).

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isImport"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> typing.Optional[ResourceNode]:
        '''(experimental) Reference to the L2 Resource that wraps this L1 CfnResource if it is wrapped.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[ResourceNode], jsii.get(self, "resource"))


class Dependency(
    Edge,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-prototyping-sdk/cdk-graph.Dependency",
):
    '''(experimental) Dependency edge class defines CloudFormation dependency between resources.

    :stability: experimental
    '''

    def __init__(self, props: ITypedEdgeProps) -> None:
        '''
        :param props: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fd372e4374fd97c2063ed328c8510e6206d687926630586aa84b7ceefad0487)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isDependency")
    @builtins.classmethod
    def is_dependency(cls, edge: Edge) -> builtins.bool:
        '''(experimental) Indicates if given edge is a {@link Dependency} edge.

        :param edge: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c39bae972244929da44f4c0a3a1600b31cc463e3302b521d8d4b7222c4f25adf)
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isDependency", [edge]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PREFIX")
    def PREFIX(cls) -> builtins.str:
        '''(experimental) Edge prefix to denote dependency edge.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PREFIX"))


@jsii.interface(jsii_type="@aws-prototyping-sdk/cdk-graph.INestedStackNodeProps")
class INestedStackNodeProps(IStackNodeProps, typing_extensions.Protocol):
    '''(experimental) {@link NestedStackNode} props.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="parentStack")
    def parent_stack(self) -> StackNode:
        '''(experimental) Parent stack.

        :stability: experimental
        '''
        ...


class _INestedStackNodePropsProxy(
    jsii.proxy_for(IStackNodeProps), # type: ignore[misc]
):
    '''(experimental) {@link NestedStackNode} props.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph.INestedStackNodeProps"

    @builtins.property
    @jsii.member(jsii_name="parentStack")
    def parent_stack(self) -> StackNode:
        '''(experimental) Parent stack.

        :stability: experimental
        '''
        return typing.cast(StackNode, jsii.get(self, "parentStack"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INestedStackNodeProps).__jsii_proxy_class__ = lambda : _INestedStackNodePropsProxy


class ImportReference(
    Reference,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-prototyping-sdk/cdk-graph.ImportReference",
):
    '''(experimental) Import reference defines **Fn::ImportValue** type reference edge.

    :stability: experimental
    '''

    def __init__(self, props: ITypedEdgeProps) -> None:
        '''
        :param props: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__350f2f33144e15bd181485e2e8bc89d6579e6999609446cd52d3840a5acd93a8)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isImport")
    @builtins.classmethod
    def is_import(cls, edge: Edge) -> builtins.bool:
        '''(experimental) Indicates if edge is **Fn::ImportValue** based {@link Reference}.

        :param edge: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bdaa040d5ae5a8017a9488e85a16b62432ccc019c4be660ab26ad017b1dd65e)
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isImport", [edge]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PREFIX")
    def PREFIX(cls) -> builtins.str:
        '''(experimental) Edge prefix to denote **Fn::ImportValue** type reference edge.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PREFIX"))


class NestedStackNode(
    StackNode,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-prototyping-sdk/cdk-graph.NestedStackNode",
):
    '''(experimental) NestedStackNode defines a cdk NestedStack.

    :stability: experimental
    '''

    def __init__(self, props: INestedStackNodeProps) -> None:
        '''
        :param props: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98b7a136fe981a76203feb9614598691fbec0a90bb99d69337d335cfe5bb8f26)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isNestedStackNode")
    @builtins.classmethod
    def is_nested_stack_node(cls, node: Node) -> builtins.bool:
        '''(experimental) Indicates if node is a {@link NestedStackNode}.

        :param node: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7747ea11b954476b4e602b80dad163e930f4bf85473dcbf95d794e1f927f23c8)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isNestedStackNode", [node]))

    @jsii.member(jsii_name="mutateHoist")
    def mutate_hoist(self, new_parent: Node) -> None:
        '''(experimental) Hoist *this node* to an *ancestor* by removing it from its current parent node and in turn moving it to the ancestor.

        :param new_parent: -

        :stability: experimental
        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ada9679f61550414fe34e5dfee0d2c546c4467c383363f80d32b45d7dd7deb9)
            check_type(argname="argument new_parent", value=new_parent, expected_type=type_hints["new_parent"])
        return typing.cast(None, jsii.invoke(self, "mutateHoist", [new_parent]))

    @builtins.property
    @jsii.member(jsii_name="parentStack")
    def parent_stack(self) -> typing.Optional[StackNode]:
        '''(experimental) Get parent stack of this nested stack.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[StackNode], jsii.get(self, "parentStack"))


__all__ = [
    "AppNode",
    "AttributeReference",
    "BaseEntity",
    "CdkConstructIds",
    "CdkGraph",
    "CdkGraphArtifact",
    "CdkGraphArtifacts",
    "CdkGraphContext",
    "CfnAttributesEnum",
    "CfnResourceNode",
    "ConstructInfo",
    "ConstructInfoFqnEnum",
    "Dependency",
    "Edge",
    "EdgeDirectionEnum",
    "EdgeTypeEnum",
    "FilterPreset",
    "FilterStrategy",
    "FlagEnum",
    "IAppNodeProps",
    "IAttributeReferenceProps",
    "IBaseEntityDataProps",
    "IBaseEntityProps",
    "ICdkGraphPlugin",
    "ICdkGraphProps",
    "ICfnResourceNodeProps",
    "IEdgePredicate",
    "IEdgeProps",
    "IFilterFocusCallback",
    "IFindEdgeOptions",
    "IFindNodeOptions",
    "IGraphFilter",
    "IGraphFilterPlan",
    "IGraphFilterPlanFocusConfig",
    "IGraphPluginBindCallback",
    "IGraphReportCallback",
    "IGraphStoreFilter",
    "IGraphSynthesizeCallback",
    "IGraphVisitorCallback",
    "INestedStackNodeProps",
    "INodePredicate",
    "INodeProps",
    "IOutputNodeProps",
    "IParameterNodeProps",
    "IReferenceProps",
    "IResourceNodeProps",
    "ISerializableEdge",
    "ISerializableEntity",
    "ISerializableGraphStore",
    "ISerializableNode",
    "IStackNodeProps",
    "IStoreCounts",
    "ITypedEdgeProps",
    "ITypedNodeProps",
    "ImportReference",
    "InferredNodeProps",
    "MetadataTypeEnum",
    "NestedStackNode",
    "Node",
    "NodeTypeEnum",
    "OutputNode",
    "ParameterNode",
    "PlainObject",
    "Reference",
    "ReferenceTypeEnum",
    "ResourceNode",
    "RootNode",
    "SGEdge",
    "SGEntity",
    "SGGraphStore",
    "SGNode",
    "SGUnresolvedReference",
    "StackNode",
    "StageNode",
    "Store",
]

publication.publish()

def _typecheckingstub__28286f53bba3c64713566007568503857222212a302b0e060ba6e0b0d67633d0(
    root: _constructs_77d1e7e8.Construct,
    *,
    plugins: typing.Optional[typing.Sequence[ICdkGraphPlugin]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23a3bf1400984efa0d22219618f9f7c2b1b3cf1e07948dc134f293b4b7c2799d(
    *,
    filename: builtins.str,
    filepath: builtins.str,
    id: builtins.str,
    source: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__989da9e5b172457303b3aef4ed9ac17f179950db8e46d91724cfbd2bef74748c(
    store: Store,
    outdir: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__816d6f7e514bec099b526e77f33ac86bf42b1f7c17752bd722a51497ead76673(
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1a00986a437e5e797c994f6208b3c343e30d18bbaace95f147963e9d81cadaa(
    filename: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7076e52c64c67503ac32339aed9bc664c32f9a2ddb2e991c39310e6ef95f54e(
    source: typing.Union[CdkGraph, ICdkGraphPlugin],
    id: builtins.str,
    filepath: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46503812b23f70feadc9d32271563a9cd498878137bf496eb61bc3691922e6e9(
    source: typing.Union[CdkGraph, ICdkGraphPlugin],
    id: builtins.str,
    filename: builtins.str,
    data: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0075161e9afebef046d274d60dcc85233e4fdd2bc46a8916a19dd21ded5d2e1a(
    *,
    fqn: builtins.str,
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54a2cc255662b5e0876e8d0db605a73b801eab0609f7115a372a87534496cb3e(
    value: IGraphPluginBindCallback,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22f4e280b8570ce4b34179d204a45f016fc59269a033e588b8034098b2fd8a72(
    value: typing.Optional[IGraphVisitorCallback],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc2ff5d90cebb53054076da0d81c370dce67943e3aa06c8a1acd6778dc66ded6(
    value: typing.Optional[IGraphReportCallback],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f284eaa765a86f8c6ceacf14f7621e610187a734600a8597ddf791545b56252(
    value: typing.Optional[IGraphSynthesizeCallback],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1029a75fabb2077855ce3cf42d58afba32e0ebd9b55995166d157a280e84bc8a(
    *,
    plugins: typing.Optional[typing.Sequence[ICdkGraphPlugin]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__440664ecfc99fe6d91fc2446a1d9edaebf3ec63fe4d2dde7ac509deaa8835a48(
    value: typing.Optional[_constructs_77d1e7e8.ConstructOrder],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c042bf96af1e885eb3a18d82be6e0e70cb7275544df14fe112ecef0343ff731(
    value: typing.Optional[IEdgePredicate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ae17a56aa13539018155b42cba0bfdb979e49216bdb763a0858a65e139a8539(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a17706617442c90e6363c950cb20ba8f09e96181e25fb5918d0dff8c468242e(
    value: typing.Optional[_constructs_77d1e7e8.ConstructOrder],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0600443b4cf948de4ef4854854b1f2c81d19ca55dd180c8a00faf7563eeccfa2(
    value: typing.Optional[INodePredicate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6241e99a37312065c459cc9683e037e64c397e027b88a5b903d7cbabb1ac8ea(
    *,
    node: typing.Union[Node, IFilterFocusCallback],
    no_hoist: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc362a68986d00030e674b435fe815be827570aa7f8a93400db488245da5a627(
    *,
    uuid: builtins.str,
    attributes: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]]]]]]] = None,
    flags: typing.Optional[typing.Sequence[FlagEnum]] = None,
    metadata: typing.Optional[typing.Sequence[typing.Union[_constructs_77d1e7e8.MetadataEntry, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf966f76b2c4db416b9d33d4b216fd881dc8b2fade8b9cf53ee5938a99e87b45(
    *,
    edges: typing.Sequence[typing.Union[SGEdge, typing.Dict[builtins.str, typing.Any]]],
    tree: typing.Union[SGNode, typing.Dict[builtins.str, typing.Any]],
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1f023a3fe8a734d710d6155e34fc386bdcd7777295273f810fb4335bf7750f3(
    *,
    uuid: builtins.str,
    attributes: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]]]]]]] = None,
    flags: typing.Optional[typing.Sequence[FlagEnum]] = None,
    metadata: typing.Optional[typing.Sequence[typing.Union[_constructs_77d1e7e8.MetadataEntry, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    id: builtins.str,
    node_type: NodeTypeEnum,
    path: builtins.str,
    cfn_type: typing.Optional[builtins.str] = None,
    children: typing.Optional[typing.Mapping[builtins.str, typing.Union[SGNode, typing.Dict[builtins.str, typing.Any]]]] = None,
    construct_info: typing.Optional[typing.Union[ConstructInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    edges: typing.Optional[typing.Sequence[builtins.str]] = None,
    logical_id: typing.Optional[builtins.str] = None,
    parent: typing.Optional[builtins.str] = None,
    stack: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__093efbca62496222f83dc4c926674b4af60ecc878556c3dc198dc6a5a6e2fc8f(
    *,
    reference_type: ReferenceTypeEnum,
    source: builtins.str,
    target: builtins.str,
    value: typing.Optional[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c0791921f25556bbc2c8164d44d2289761731e68c2598a9cba96f175f256a73(
    allow_destructive_mutations: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ded7d912211e7b50ae46a74ae7bf9b68ce262a10ed352fa6b3eb9553a668baa(
    edge: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbaabc9ec5dfc8d77fe2479d07f0f1c17e60a13e8d6f57804dbb9d93d470ad39(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15c6a25d652e9961baf37dad48966d941983042cd9bbdd23a6f07ee97e4976a5(
    stack: StackNode,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e65b41882a8ab0b9d784a00e3fc56d3701a36386ebb7cfea42f2aeeb5ec1e836(
    stage: StageNode,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebc9b96e7664c6e4ab1e6760d98dd03bcb42b46f6eed7a831092a894c072aa7c(
    allow_destructive_mutations: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79fd3c45504b00281faf400a4966b73587a2e09d9ae05c73a23eaae2d6a1e670(
    stack: StackNode,
    logical_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee6be88664b09024a938ab1084f8eaf5be8582aff6546f7694717d08183a4001(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52f242e9533d8e3603727048cefca8ca1bcd7283fbb68e8936a31f8e864f67be(
    stack: StackNode,
    logical_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d15c19e972edf54940811c986029f8d06860695359ffc2b2989380610eeab001(
    uid: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7341fe8d2ac9a3e0b0f7460cb73d249ebdb7018202421d3652103d29f4036f53(
    uuid: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7172fc8d20040a0c391f68e341f9e854387e13c14ae068ebac677842b8124065(
    uuid: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__016717b7d191ac618ce7ab95e30ef8a41c17d43bd9ee26a45afafe16d1256f43(
    uuid: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fe9441b824214f582207d4a5c1dc9ee06de01c0bc48e2b6d064b4be3e80ce8f(
    uuid: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c44d23129ef772a7abc7b7904eedb0e3dbbe5ebfd71bcb42ad1a66ea0460faa4(
    edge: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38f7f1a83926596fce68c62565a99f012d7bc267acf4a5a03b71046728afe3d6(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e82913f930cef17665caa74719684fe7d809e372cdf2e431606583476c790b3(
    arn_token: builtins.str,
    resource: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2998c0c7a2e8dcd67ac8d652f362598ce19a1470d35a293e301a2eb8c1bf538(
    stack: StackNode,
    logical_id: builtins.str,
    resource: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f2dc8f4d32f710e529c384ec54c4cf717f5cda309c0fbb212fcb4ec157460ec(
    props: IBaseEntityProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fca287acaf0ea58ee6af4324bcf355d6fbcc074e558618b8b9aab6043f9cdc48(
    key: builtins.str,
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9768f3202dfe93bb291e58985f3ddfcff7092cc72d09f07d2c7accffea6dc694(
    flag: FlagEnum,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f98067f797cee431477c28fc9918bfc97075cec47a7b28b509fbbe24def0e110(
    metadata_type: builtins.str,
    data: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de490f4f63ecc3c4c21281b57fefef64c596b89d0a42c7832eed3312545b98a0(
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__629d2e98b9f8de442a0a82d787ea97652535803463fe7587b1a46393f30ed41f(
    data: IBaseEntityDataProps,
    overwrite: typing.Optional[builtins.bool] = None,
    apply_flags: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c515cfd427885e594cc73e0ea60decf39cad8cd383f956aea551522a9607b37c(
    metadata_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bb48787831bd62ba9cc6ec3cd4f437ccd2ca6b10c99437de64f5495a63fd95b(
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a90ad630d55a7c76dd403474c2f494d2e8b9e8ec9b19e11ff4058ba19f6ef1df(
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f7d28526dd59cd5f90985af0ba144e8702a6173d9b802954abd3282f2881676(
    key: builtins.str,
    value: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3740112f7f676b6a1901f67d18ecfbd6e0fb5275c0ae459d16bba2ac64eb0f1(
    flag: FlagEnum,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff2f2591cae9b57daf46cbecf90260a471ad4c33792b0e2bb633a049e6bad804(
    metadata_type: builtins.str,
    data: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffd521f5bd58d4907c987a3aafd2a00b78000a562aa35196fbee89ee1abedae6(
    key: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61fb0de9c3c8ece2d2ee10210afc2406cd59f4f9003365b070efe806159b7e39(
    key: builtins.str,
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ef46876bb2da2fab39362139ee1fa2ecf28ef8f4790d71956b03762c2858f9f(
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1b7b9c43f39c888d029ce6474749d13f8d3f6ea07e24ac2c73ede95e3d761ec(
    strict: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc9940e76afa1f2a2a51af4a715cfc9ec8068b84e181427a075f3f950c7a75b4(
    props: IEdgeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ba3c56cfbafe629bc5c97a1b8d94b2fa09bf263f48a13e19d3273aab0c213f5(
    chain: typing.Sequence[typing.Any],
    predicate: IEdgePredicate,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d546855bb2ebbdf3c8f720ce8776a03968b65f340cea5fbbb408991981a9bb6(
    chain: typing.Sequence[typing.Any],
    predicate: IEdgePredicate,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c82d13d6d343f7daed5a05240546435a89e5e3beba9ca7e59942f57874a8a60(
    edge: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1806a9f734343b301c800fcc47acf0d01e612fca77d79b44938d9e1e3bde48ad(
    edge: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c054019cea048023a1223d0f4340b9012468fa648505eaeb18f3a309574034c4(
    _strict: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9381ac56f06abe54b86023ee566cee97fbe66d927f289a01c168fa96bdc89be4(
    direction: EdgeDirectionEnum,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__725116b7334022c2e38d2495b1c2fea7a1a1e3bfce318823076d2d73e32b4e2b(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f074e21e7d8f7ba613f207b1351316f3834cc0276f4d34070b3f84fc73ca6de2(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b19f3c99c1010b7e42cbb686da8f9795320e98e9f3a0384ef6e4c6d29f33d2b(
    value: typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34855dc7b232fc8d813a1b62cdcdd54bcbb46b14402f35ecd54aab1f79be69a4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2e86175e2d1b5d420625acfdb4a456691dd03d9008fbcf378db33eecd318cfe(
    value: typing.Optional[NodeTypeEnum],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59d7bc44379b4c689592001d4e5ab142c8f56c533b1ce7da958b1f9a0e3c0149(
    value: typing.Optional[ReferenceTypeEnum],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26cde6447d66f5a35ac630eb24e426e3c519cb621e706720d313cd85ca412122(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14ac61e4840795aa21b772948740dfece254d05e6c034663ae54ca236dcd015d(
    value: typing.Optional[NodeTypeEnum],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcdd9af99464b5c5d6c5f4a91b9bfd01b43db3776a90c811162abfcf1dd1e197(
    value: typing.Optional[NodeTypeEnum],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc702434f9098ad5400a36b4d5fa85826622b6657d1dd0f3392de0bcab361f2c(
    *,
    uuid: builtins.str,
    attributes: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]]]]]]] = None,
    flags: typing.Optional[typing.Sequence[FlagEnum]] = None,
    metadata: typing.Optional[typing.Sequence[typing.Union[_constructs_77d1e7e8.MetadataEntry, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    dependencies: typing.Sequence[builtins.str],
    unresolved_references: typing.Sequence[typing.Union[SGUnresolvedReference, typing.Dict[builtins.str, typing.Any]]],
    cfn_type: typing.Optional[builtins.str] = None,
    construct_info: typing.Optional[typing.Union[ConstructInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    logical_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74fba1b214a0b6da2c81857be0f084091ee35bd210c9a55c3fd5e104e3e0dec4(
    props: INodeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3da87100250635b0c50af6bdcd03a86edd18d0aac4df75ad9acc23cb03167b76(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fecabe827c1e09a7a8c0b545f904fd63ceded0137ef9c59c283bad92192b8779(
    edge: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f652daee515413ba0e936bdd57028711a6f6d1e07a4732025f7a58047ee1f599(
    edge: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8fce1a47ea1104d69fc39fdeaf2352f4c88133185dff4b085c03fdcdd5cf4de(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d30c20ae909df3aaed77d3c61ddb29622905d2cf8b95df8eb73d4f7cc5fe4a9a(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5987c16db88320ba918a789572bee8884821f66266adc3461833f3808b51611(
    predicate: INodePredicate,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68abed2aa07ec0b51cf326a6d40ccc90857dcc58aa8602d6fe3a4c95428f7529(
    options: typing.Optional[IFindNodeOptions] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7f0f74c30a800cda16150fb9dd37ffff3569b44fb0decf754a0b52b58fb0216(
    options: typing.Optional[IFindEdgeOptions] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c48bf8b6d829071f27f765fa51569e4816e62af749fb1380a1adb9b327209649(
    predicate: INodePredicate,
    max: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1250fde13da19383a24377937a8e3da9c1dac10eaf648f088df319d8d95aaf5(
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6751959dbf5836b0001e27458851fb4102db4a1cd85ed0612c9609062b59e1d8(
    predicate: IEdgePredicate,
    reverse: typing.Optional[builtins.bool] = None,
    follow: typing.Optional[builtins.bool] = None,
    direct: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb69053fa918bf283e62a41638c10b714ca12d8a7c133e8eff448d274828f91e(
    predicate: IEdgePredicate,
    reverse: typing.Optional[builtins.bool] = None,
    follow: typing.Optional[builtins.bool] = None,
    direct: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a71ef48e84e46dc216625c429813b383dfdcdf3dcbaa7da531fa9f8a8b95d8a3(
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4ad2e0d7a748a08d49142472755ec0a258b78c24707aa0873d4eb150abb5c74(
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aa874e5b7d5b668ae367553a55f5db22d91f39d582e443f65eeb7b8b8e21e85(
    reverse: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea903bfc5fb1ce19d9fb323a51a92834bd520d5834c12419ee4fddeb0d750330(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0b1c27a0709375706f73127e248dfbda0cbab1ead7faf39dfe11be7a1226cfc(
    ancestor: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bd700d653ffb5a3352a6639c715f3cb25552651b3504110d9d3fb9583c9c233(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2575a885febef02fb0b0e973913fe6b8ee79fdba778ca87f62f1b1c83b2bfe0(
    ancestor: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9b18468fcf94a48458d4d3eeb8cfde1c9322a2508820c8ada0cc9e48a8a8658(
    strict: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d56c8215efb5ab6998320a2aa4edaa2cf82014505476153fb15524d6cc65441c(
    new_parent: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deada882d081798a49ca7dadca89fbf1032b8eb25cdc7f98541af185cd7fe5cf(
    new_parent: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9054f48201348fe56a5b872785512bfc264c9b97152917a97ec019d68ef6890(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6dd90ba9fb9c195c8498aa32ac50c1e8008d173cb87ed535f21dbe835ff1309(
    link: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcc8ef830bc8b60569c5d33ea798ceb1607d531edba6cb7907677008c0fffbdb(
    link: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3da145a8289db66b0d336f3e315bdf68451e5f68af71ee47e03d07f6e5c4a4a4(
    props: IOutputNodeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a127ae0d40eecf96bdf403e311388722667e462513fbf566c60d8e6f58539cfa(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e55e96ec84c6585331429d9addc5c1ebf5414133101eb4528626f9042720eb4f(
    strict: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6bad65a471e15f8ee779034629700c50cdf0c04cb7d2dcd091132895e2aa49f(
    props: IParameterNodeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__621af1c40617acac1c635f63f857e3dfdbe754e7f7f5ac44edc794f02cc8aa62(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc8f87ea7f23941a2ade0f5147d5a9c62e340781cc71ac5a027cbeb1f90f8760(
    strict: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13cbf6dec7094f31d6fc6f739bbf44b5b4b63d0b0a6b3862a1a164c86b374cde(
    props: IReferenceProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdce1dd0ab4d7b2d805c4d9711b42f8cdb82da30805f659d176efe9f34594d2d(
    edge: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8c12e3117f04b4e98b681272a904b6082dce26884c1976de71fdba4e42603f7(
    edge: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c6c9f4ced42ead844dc1054e31bd1b78f4e8e0d0b252cb49ab29ea9a39ea70b(
    props: IResourceNodeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0453f99caba49f66a98152ee3485b1bf8866146a898149773967a2c0bc2f6dac(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f0870fe328fea4963f5221f2a3c0f0496fe542e20c7804c93866e881daec5d4(
    cfn_resource: typing.Optional[CfnResourceNode] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31ffb4369b94961c7784bf8d2b3fe8b642d68211d9339037a9aa3f8672ea96c3(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2858e1c353684c85393980ddd8171e738a810cdb39195bdd4b1fc5a5129877f4(
    store: Store,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a94129a7134d7f30f6f7df7c59273964794f931bc432072d1d3cdafed475f2d(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52135bc8e4aa332f0c9ae263f6b1f3b0171e5b60a962c50cda9981f7cd12b769(
    options: typing.Optional[IFindNodeOptions] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70cddb7519cff2871f863c6cd3e0249639b48424c7127867dba034a8dcb68e1f(
    _ancestor: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de6bbc2b0a38053065cef3efa2294d4187e740588afc3ded564fc359f94245c2(
    _strict: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d4a7bad4f9d7ba1fd95de784e042abc8d2fca9c2352f2626b664afd09d1652f(
    _new_parent: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e6e44c6ff3c944799ca44f751aee392acaa420b9a44b401db722bf60be6a51e(
    *,
    uuid: builtins.str,
    attributes: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]]]]]]] = None,
    flags: typing.Optional[typing.Sequence[FlagEnum]] = None,
    metadata: typing.Optional[typing.Sequence[typing.Union[_constructs_77d1e7e8.MetadataEntry, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    direction: EdgeDirectionEnum,
    edge_type: EdgeTypeEnum,
    source: builtins.str,
    target: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c406dbfcbf0e87f9fb3c3b858a4c75940a4979183139c582777ed42545ffc8d(
    props: IStackNodeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c115a0983440348d31ae427389290c8619bdbc92e3c99929796ed50695aa950f(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__915f11470d516a7f8701600fa93eff5ba4671cdccd560f50667a796863bec880(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49ca515fbc945e2ec37d58c6ce8e826d049ebedbdb7a9ad6e414502e213b1ca5(
    node: OutputNode,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03facf341abc9ea1d0cc8d187a70c5a1eecdc35758cc5c772206af6629d5a3d1(
    node: ParameterNode,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1a6a8c26e687161d550aa54c20c52e9ce74e768edb15bffb12e2c5d7cd35ebc(
    logical_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33dc300f7e88e048c333d0f73c36a0cb5650500af888901a74cdca29eaa5f47b(
    parameter_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4728fd8b6c5b6dad937d4d5029f42a9d43d95d2bb8fa97c5dd6c0a831fc0e5cc(
    strict: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb94dd9f583fcaea84f5de0db1cd5e8dfce57b1e8c54483769c4dc8e97687fb2(
    new_parent: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21c7e2103930b4528e19756f0d2147608cc076167cd22be28f088c7faf602d3a(
    node: OutputNode,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77dcc17a3ce0b81b743d5659ee012e356bdcc6bc70eef717249ef76b3bfe64a0(
    node: ParameterNode,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcaf74ca37e625ffeed9d5a60c5941b594c1d056c261a203d0ff7aae64286f1f(
    props: ITypedNodeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeb6a55a082be98aa517799c51da665a5caae79ff73869e9bd2c23b62e8651ed(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c264d84efa90db43f239ad81dcb04b7271c5e764e17e01b895d86f1dca6bcd2(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeb1552ad75e63308b0fecbac20851396abc4f79f77267a45c3661a9920b0360(
    stack: StackNode,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17fef2232e4c6702e399a03209088941244a15f0663c7fdc456a9386c4035036(
    stack: StackNode,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b54478d4eff82d80f3fa3c12926f6c1eb7d1cbbba5cf0d54104c45ba8d2932da(
    props: IAppNodeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__337b277c4153037ed28c9def7def7aad44b9178fbe02bc5babf708d344a92c26(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0563f317c98960c719cf66869e770302bcc324f313aee0ef635224e07ce1e633(
    props: IAttributeReferenceProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dac13a68a078eda02db5a11164b8f3e3c55dc0dbabb4ec1d988c11b8a2a6310(
    edge: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__475b66da39f8ade9b8105ab8da9507c2cee4dfaea064d6e21a560fcb4a77214a(
    props: ICfnResourceNodeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2c3aed894ebb341f41635244c6a2f64947719e15b0cc56970b21706635d9a9b(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__374ac098fdc910e98fa76178b8f501b519407c242f829d1e95e81c1d11096047(
    resource: ResourceNode,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d5a2459368e54cc121bca01b26d4f7b45053e99925670e317a889e82b943cca(
    strict: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fd372e4374fd97c2063ed328c8510e6206d687926630586aa84b7ceefad0487(
    props: ITypedEdgeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c39bae972244929da44f4c0a3a1600b31cc463e3302b521d8d4b7222c4f25adf(
    edge: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__350f2f33144e15bd181485e2e8bc89d6579e6999609446cd52d3840a5acd93a8(
    props: ITypedEdgeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bdaa040d5ae5a8017a9488e85a16b62432ccc019c4be660ab26ad017b1dd65e(
    edge: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98b7a136fe981a76203feb9614598691fbec0a90bb99d69337d335cfe5bb8f26(
    props: INestedStackNodeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7747ea11b954476b4e602b80dad163e930f4bf85473dcbf95d794e1f927f23c8(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ada9679f61550414fe34e5dfee0d2c546c4467c383363f80d32b45d7dd7deb9(
    new_parent: Node,
) -> None:
    """Type checking stubs"""
    pass
