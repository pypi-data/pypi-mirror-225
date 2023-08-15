'''
## Diagram Plugin - Cdk Graph

`@aws-prototyping-sdk/cdk-graph-plugin-diagram`

![experimental](https://img.shields.io/badge/stability-experimental-orange.svg)
![alpha](https://img.shields.io/badge/version-alpha-red.svg) \
[![API Documentation](https://img.shields.io/badge/view-API_Documentation-blue.svg)](https://aws.github.io/aws-prototyping-sdk/typescript/cdk-graph-plugin-diagram/index.html)
[![Source Code](https://img.shields.io/badge/view-Source_Code-blue.svg)](https://github.com/aws/aws-prototyping-sdk/tree/mainline/packages/cdk-graph-plugin-diagram)

This plugin generates diagrams utilizing the [cdk-graph](https://aws.github.io/aws-prototyping-sdk/typescript/cdk-graph/index.html) framework.

> More comprehensive documentation to come as this package stabilizes.

> **Disclaimer:** This is the first **cdk graph** plugin, it is highly *experimental*, and subject to major refactors as we gain feedback from the community.

> **BREAKING CHANGES** (pre-release)
>
> * `<= v0.14.8`: Only the last stage of a multi stage app will be rendered by default, which is commonly the production stage. Use the `theme.rendering.stage` config option to override this for each graph or in defaults.

|                                                                            |                                                                         |
| -------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| <img src="docs/assets/cdk-graph-plugin-diagram/default.png" width="300" /> | <img src="docs/assets/cdk-graph-plugin-diagram/dark.png" width="300" /> |

### Quick Start

```python
// bin/app.ts

// Must wrap cdk app with async IIFE function to enable async cdk-graph report
(async () => {
  const app = new App();
  // ... add stacks, etc
  const graph = new CdkGraph(app, {
    plugins: [new CdkGraphDiagramPlugin()],
  });

  app.synth();

  // async cdk-graph reporting hook
  await graph.report();
})();

// => cdk.out/diagram.dot
// => cdk.out/diagram.svg
// => cdk.out/diagram.png
```

> This plugin currently only supports `async report()` generation following the above example. **Make sure to wrap the cdk app with *async IIFE*.**

### Supported Formats

| Format                                          | Status                                                     | Extends                                         | Provider                            |
| ----------------------------------------------- | ---------------------------------------------------------- | ----------------------------------------------- | ----------------------------------- |
| [DOT](https://graphviz.org/docs/outputs/canon/) | ![beta](https://img.shields.io/badge/status-beta-cyan.svg) | -                                               | [Graphviz](docs/graphviz/README.md) |
| [SVG](https://graphviz.org/docs/outputs/svg/)   | ![beta](https://img.shields.io/badge/status-beta-cyan.svg) | [DOT](https://graphviz.org/docs/outputs/canon/) | [Graphviz](docs/graphviz/README.md) |
| [PNG](https://graphviz.org/docs/outputs/png/)   | ![beta](https://img.shields.io/badge/status-beta-cyan.svg) | [SVG](https://graphviz.org/docs/outputs/canon/) | [Graphviz](docs/graphviz/README.md) |

---


### Diagram Providers

| Provider                            | Status                                                         | Formats                                                                                                                                       |
| ----------------------------------- | -------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| [Graphviz](docs/graphviz/README.md) | ![alpha](https://img.shields.io/badge/status-alpha-orange.svg) | [DOT](https://graphviz.org/docs/outputs/canon/), [SVG](https://graphviz.org/docs/outputs/svg/), [PNG](https://graphviz.org/docs/outputs/png/) |
| [Drawio](docs/drawio/README.md)     | ![design](https://img.shields.io/badge/status-design-tan.svg)  | *TBD: very early stage design and development*                                                                                                |

---


### Configuration

See [IPluginConfig](https://aws.github.io/aws-prototyping-sdk/typescript/cdk-graph-plugin-diagram/index.html#ipluginconfig) interface for details, and look in [unit tests](https://github.com/aws/aws-prototyping-sdk/tree/mainline/packages/cdk-graph-plugin-diagram/test/graphviz) for additional examples.

By default the diagram plugin will generate a single "compact" preset diagram.
It is capable of creating multiple diagrams each with different configurations, as well as defining the defaults to use.

**Defaults Option**

Changing the `defaults` option will modify default options for all diagrams, including the default diagram.

> See [IDiagramConfigBase](https://aws.github.io/aws-prototyping-sdk/typescript/cdk-graph-plugin-diagram/index.html#idiagramconfigbase) interface for `plugin.defaults` options.

```python
new CdkGraphDiagramPlugin({
  defaults: {
    theme: "dark",
    filterPlan: {
      preset: FilterPreset.NONE,
    },
  },
});

// => results in a single diagram that is "verbose" and "dark", since no resources are filtered
```

**Diagrams Option**

By modifying the `diagrams` option of the plugin you have full control over the rendering of diagrams, and can render **multiple** diagrams.

> See [IDiagramConfig](https://aws.github.io/aws-prototyping-sdk/typescript/cdk-graph-plugin-diagram/index.html#idiagramconfig) interface for diagram config options.

```python
new CdkGraphDiagramPlugin({
  diagrams: [
    {
      name: "diagram-1",
      title: "Diagram 1 (dark + compact)",
      theme: "dark",
      // the default `filterPlan: { preset: FilterPreset.COMPACT }` will still apply
    },
    {
      name: "diagram-2",
      title: "Diagram 2 (dark + verbose)",
      theme: "dark",
      filterPlan: {
        preset: FilterPreset.NONE,
      },
    },
    {
      name: "diagram-3",
      title: "Diagram 3 (no defaults)",
      ignoreDefaults: true, // default options will not be applied (theme, filterPlan, etc)
    },
  ],
});
```

#### Example Diagram Configs (expand below)

The below examples define individual diagram configs in the `diagrams` options of the plugin as described above.

```python
new CdkGraphDiagramPlugin({
  diagrams: [
    // ... insert diagram  config(s) here - see below for examples
  ],
});
```

##### **Presets**

<details>
<summary>Preset: compact</summary>

[<img src="docs/assets/cdk-graph-plugin-diagram/compact.png" height="200" />](docs/assets/cdk-graph-plugin-diagram/compact.png)

```python
{
  name: "compact",
  title: "Compact Diagram",
  filterPlan: {
    preset: FilterPreset.COMPACT,
  },
},
```

</details><details>
<summary>Preset: verbose</summary>

[<img src="docs/assets/cdk-graph-plugin-diagram/verbose.png" height="200" />](docs/assets/cdk-graph-plugin-diagram/verbose.png)

```python
{
  name: "verbose",
  title: "Verbose Diagram",
  format: DiagramFormat.PNG,
  ignoreDefaults: true,
},
```

</details>

##### **Focus**

<details>
<summary>Focus: hoist</summary>

[<img src="docs/assets/cdk-graph-plugin-diagram/focus.png" height="200" />](docs/assets/cdk-graph-plugin-diagram/focus.png)

```python
{
  name: "focus",
  title: "Focus Lambda Diagram (non-extraneous)",
  filterPlan: {
    focus: (store) =>
      store.getNode(getConstructUUID(app.stack.lambda)),
    preset: FilterPreset.NON_EXTRANEOUS,
  },
  ignoreDefaults: true,
},
```

</details><details>
<summary>Focus: no hoist</summary>

[<img src="docs/assets/cdk-graph-plugin-diagram/focus-nohoist.png" height="200" />](docs/assets/cdk-graph-plugin-diagram/focus-nohoist.png)

```python
{
  name: "focus-nohoist",
  title: "Focus WebServer Diagram (noHoist, verbose)",
  filterPlan: {
    focus: {
      node: (store) =>
        store.getNode(getConstructUUID(app.stack.webServer)),
      noHoist: true,
    },
  },
  ignoreDefaults: true,
},
```

</details>

##### **Filters**

<details>
<summary>Filter: Include specific cfn resource types</summary>

[<img src="docs/assets/cdk-graph-plugin-diagram/filter-cfntype-include.png" height="200" />](docs/assets/cdk-graph-plugin-diagram/filter-cfntype-include.png)

```python
{
  name: "includeCfnType",
  title: "Include CfnType Diagram (filter)",
  filterPlan: {
    filters: [
      Filters.includeCfnType([
        aws_arch.CfnSpec.ServiceResourceDictionary.EC2.Instance,
        /AWS::Lambda::Function.*/,
        "AWS::IAM::Role",
      ]),
      Filters.compact(),
    ],
  },
},
```

</details><details>
<summary>Filter: Exclude specific cfn resource types</summary>

[<img src="docs/assets/cdk-graph-plugin-diagram/filter-cfntype-exclude.png" height="200" />](docs/assets/cdk-graph-plugin-diagram/filter-cfntype-exclude.png)

```python
{
  name: "excludeCfnType",
  title: "Exclude CfnType Diagram (filter)",
  filterPlan: {
    filters: [
      Filters.excludeCfnType([
        /AWS::EC2::VPC.*/,
        aws_arch.CfnSpec.ServiceResourceDictionary.IAM.Role,
      ]),
      Filters.compact(),
    ],
  },
},
```

</details><details>
<summary>Filter: Include specific graph node types</summary>

[<img src="docs/assets/cdk-graph-plugin-diagram/filter-nodetype-include.png" height="200" />](docs/assets/cdk-graph-plugin-diagram/filter-nodetype-include.png)

```python
{
  name: "includeNodeType",
  title: "Include NodeType Diagram (filter)",
  filterPlan: {
    filters: [
      Filters.includeNodeType([
        NodeTypeEnum.STACK,
        NodeTypeEnum.RESOURCE,
      ]),
      Filters.compact(),
    ],
  },
},
```

</details><details>
<summary>Filter: Include specific graph node types</summary>

[<img src="docs/assets/cdk-graph-plugin-diagram/filter-nodetype-include.png" height="200" />](docs/assets/cdk-graph-plugin-diagram/filter-nodetype-include.png)

```python
{
  name: "includeNodeType",
  title: "Include NodeType Diagram (filter)",
  filterPlan: {
    filters: [
      Filters.includeNodeType([
        NodeTypeEnum.STACK,
        NodeTypeEnum.RESOURCE,
      ]),
      Filters.compact(),
    ],
  },
},
```

</details><details>
<summary>Filter: Exclude specific graph node types</summary>

[<img src="docs/assets/cdk-graph-plugin-diagram/filter-nodetype-exclude.png" height="200" />](docs/assets/cdk-graph-plugin-diagram/filter-nodetype-exclude.png)

```python
{
  name: "excludeNodeType",
  title: "Exclude NodeType Diagram (filter)",
  filterPlan: {
    filters: [
      Filters.excludeNodeType([
        NodeTypeEnum.NESTED_STACK,
        NodeTypeEnum.CFN_RESOURCE,
        NodeTypeEnum.OUTPUT,
        NodeTypeEnum.PARAMETER,
      ]),
      Filters.compact(),
    ],
  },
},
```

</details>

##### **Themes**

<details>
<summary>Theme: Dark</summary>

[<img src="docs/assets/cdk-graph-plugin-diagram/dark.png" height="200" />](docs/assets/cdk-graph-plugin-diagram/dark.png)

```python
{
  name: "Dark",
  title: "Dark Theme Diagram",
  theme: theme,
},
```

</details><details>
<summary>Theme: Dark - render service icons</summary>

[<img src="docs/assets/cdk-graph-plugin-diagram/dark-services.png" height="200" />](docs/assets/cdk-graph-plugin-diagram/dark-services.png)

```python
{
  name: "dark-services",
  title: "Dark Theme Custom Diagram",
  theme: {
    theme: theme,
    rendering: {
      resourceIconMin: GraphThemeRenderingIconTarget.SERVICE,
      resourceIconMax: GraphThemeRenderingIconTarget.CATEGORY,
      cfnResourceIconMin: GraphThemeRenderingIconTarget.DATA,
      cfnResourceIconMax: GraphThemeRenderingIconTarget.RESOURCE,
    },
  },
},
```

</details>
<details>
<summary>Theme: Dark - verbose</summary>

[<img src="docs/assets/cdk-graph-plugin-diagram/dark-verbose.png" height="200" />](docs/assets/cdk-graph-plugin-diagram/dark-verbose.png)

```python
{
  name: "dark-verbose",
  title: "Dark Theme Verbose Diagram",
  ignoreDefaults: true,
  theme: theme,
},
```

</details>---


### Next Steps

* [ ] Battle test in the wild and get community feedback
* [ ] Improve image coverage and non-image node rendering
* [ ] Add drawio support
* [ ] Add common filter patterns and helpers
* [ ] Enable generating diagrams outside of synthesis process (maybe CLI)
* [ ] Implement interactive diagram, with potential for dynamic filtering and config generation
* [ ] Support using interactive diagram as config generator for other plugins (or as separate plugin that depends on this)

---


Inspired by [cdk-dia](https://github.com/pistazie/cdk-dia) and [cfn-dia](https://github.com/mhlabs/cfn-diagram) with ❤️
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

import aws_prototyping_sdk.cdk_graph as _aws_prototyping_sdk_cdk_graph_3c35d073


@jsii.implements(_aws_prototyping_sdk_cdk_graph_3c35d073.ICdkGraphPlugin)
class CdkGraphDiagramPlugin(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-prototyping-sdk/cdk-graph-plugin-diagram.CdkGraphDiagramPlugin",
):
    '''(experimental) CdkGraphDiagramPlugin is a {@link ICdkGraphPluginCdkGraph Plugin} implementation for generating diagram artifacts from the {@link CdkGraph} framework.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Union["IDiagramConfigBase", typing.Dict[builtins.str, typing.Any]]] = None,
        diagrams: typing.Optional[typing.Sequence[typing.Union["IDiagramConfig", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param defaults: (experimental) Default configuration to apply to all diagrams.
        :param diagrams: (experimental) List of diagram configurations to generate diagrams.

        :stability: experimental
        '''
        config = IPluginConfig(defaults=defaults, diagrams=diagrams)

        jsii.create(self.__class__, self, [config])

    @jsii.member(jsii_name="artifactFilename")
    @builtins.classmethod
    def artifact_filename(
        cls,
        name: builtins.str,
        format: "DiagramFormat",
    ) -> builtins.str:
        '''(experimental) Get standardized artifact file name for diagram artifacts.

        :param name: -
        :param format: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c2c702aa641239e3944c5e390fa5500dfe4e2fb13fbc6f7273623914011bb78)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "artifactFilename", [name, format]))

    @jsii.member(jsii_name="artifactId")
    @builtins.classmethod
    def artifact_id(cls, name: builtins.str, format: "DiagramFormat") -> builtins.str:
        '''(experimental) Get standardized artifact id for diagram artifacts.

        :param name: -
        :param format: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e705150c6494bb72a14eb56acfb819db5ab9d9a3a7abf142762746a723048619)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "artifactId", [name, format]))

    @jsii.member(jsii_name="getDiagramArtifact")
    def get_diagram_artifact(
        self,
        name: builtins.str,
        format: "DiagramFormat",
    ) -> typing.Optional[_aws_prototyping_sdk_cdk_graph_3c35d073.CdkGraphArtifact]:
        '''(experimental) Get diagram artifact for a given name and format.

        :param name: -
        :param format: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c465087309222b9a22cda02d8c3dcbdae9b128b2d0c03b955c47d91810c85edc)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
        return typing.cast(typing.Optional[_aws_prototyping_sdk_cdk_graph_3c35d073.CdkGraphArtifact], jsii.invoke(self, "getDiagramArtifact", [name, format]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ARTIFACT_NS")
    def ARTIFACT_NS(cls) -> builtins.str:
        '''(experimental) Namespace for artifacts of the diagram plugin.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ARTIFACT_NS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ID")
    def ID(cls) -> builtins.str:
        '''(experimental) Fixed id of the diagram plugin.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ID"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="VERSION")
    def VERSION(cls) -> builtins.str:
        '''(experimental) Current semantic version of the diagram plugin.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "VERSION"))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> "IPluginConfig":
        '''(experimental) Get diagram plugin config.

        :stability: experimental
        '''
        return typing.cast("IPluginConfig", jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''(experimental) Unique identifier for this plugin.

        :stability: experimental
        :inheritdoc: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        '''(experimental) Plugin version.

        :stability: experimental
        :inheritdoc: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="defaultDotArtifact")
    def default_dot_artifact(
        self,
    ) -> typing.Optional[_aws_prototyping_sdk_cdk_graph_3c35d073.CdkGraphArtifact]:
        '''(experimental) Get default dot artifact.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_prototyping_sdk_cdk_graph_3c35d073.CdkGraphArtifact], jsii.get(self, "defaultDotArtifact"))

    @builtins.property
    @jsii.member(jsii_name="defaultPngArtifact")
    def default_png_artifact(
        self,
    ) -> typing.Optional[_aws_prototyping_sdk_cdk_graph_3c35d073.CdkGraphArtifact]:
        '''(experimental) Get default PNG artifact.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_prototyping_sdk_cdk_graph_3c35d073.CdkGraphArtifact], jsii.get(self, "defaultPngArtifact"))

    @builtins.property
    @jsii.member(jsii_name="dependencies")
    def dependencies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of plugins this plugin depends on, including optional semver version (eg: ["foo", "bar@1.2"]).

        :stability: experimental
        :inheritdoc: true
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dependencies"))

    @builtins.property
    @jsii.member(jsii_name="bind")
    def bind(self) -> _aws_prototyping_sdk_cdk_graph_3c35d073.IGraphPluginBindCallback:
        '''(experimental) Binds the plugin to the CdkGraph instance.

        Enables plugins to receive base configs.

        :stability: experimental
        :inheritdoc: true
        '''
        return typing.cast(_aws_prototyping_sdk_cdk_graph_3c35d073.IGraphPluginBindCallback, jsii.get(self, "bind"))

    @bind.setter
    def bind(
        self,
        value: _aws_prototyping_sdk_cdk_graph_3c35d073.IGraphPluginBindCallback,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd20e03a66d768d39dad86a2939fae03a0a2e870540db7c35a8d6f0624464fc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bind", value)

    @builtins.property
    @jsii.member(jsii_name="report")
    def report(
        self,
    ) -> typing.Optional[_aws_prototyping_sdk_cdk_graph_3c35d073.IGraphReportCallback]:
        '''(experimental) Generate asynchronous reports based on the graph.

        This is not automatically called when synthesizing CDK.
        Developer must explicitly add ``await graphInstance.report()`` to the CDK bin or invoke this outside
        of the CDK synth. In either case, the plugin receives the in-memory graph interface when invoked, as the
        CdkGraph will deserialize the graph prior to invoking the plugin report.

        :stability: experimental
        :inheritdoc: true
        '''
        return typing.cast(typing.Optional[_aws_prototyping_sdk_cdk_graph_3c35d073.IGraphReportCallback], jsii.get(self, "report"))

    @report.setter
    def report(
        self,
        value: typing.Optional[_aws_prototyping_sdk_cdk_graph_3c35d073.IGraphReportCallback],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb806c27af67b4d37164309b0a8a6b1ee2052cb809973708c60e38a73353d492)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "report", value)


@jsii.enum(jsii_type="@aws-prototyping-sdk/cdk-graph-plugin-diagram.DiagramFormat")
class DiagramFormat(enum.Enum):
    '''(experimental) Supported diagram formats that can be generated.

    Extended formats are automatically generated, for example if you generate "png" which extends
    "svg" which extends "dot", the resulting generated files will be all aforementioned.

    :stability: experimental
    '''

    DOT = "DOT"
    '''(experimental) Graphviz `DOT Language <https://graphviz.org/doc/info/lang.html>`_.

    :stability: experimental
    '''
    SVG = "SVG"
    '''(experimental) `SVG <https://developer.mozilla.org/en-US/docs/Web/SVG>`_ generated using `dot-wasm <https://hpcc-systems.github.io/hpcc-js-wasm/classes/graphviz.Graphviz.html>`_ from {@link DiagramFormat.DOT} file.

    :stability: experimental
    :extends: DiagramFormat.DOT
    '''
    PNG = "PNG"
    '''(experimental) `PNG <https://en.wikipedia.org/wiki/Portable_Network_Graphics>`_ generated using `sharp <https://sharp.pixelplumbing.com/api-output#png>`_ from {@link DiagramFormat.SVG} file.

    :stability: experimental
    :extends: DiagramFormat.SVG
    '''


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/cdk-graph-plugin-diagram.DiagramOptions",
    jsii_struct_bases=[],
    name_mapping={"title": "title", "preset": "preset", "theme": "theme"},
)
class DiagramOptions:
    def __init__(
        self,
        *,
        title: builtins.str,
        preset: typing.Optional[_aws_prototyping_sdk_cdk_graph_3c35d073.FilterPreset] = None,
        theme: typing.Optional[typing.Union["IGraphThemeConfigAlt", builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for diagrams.

        :param title: 
        :param preset: 
        :param theme: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__872e0fa6b2a1dc9dfac4874b80a6fbc55e439af2940a0bfbcbf836b0916c1a86)
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument preset", value=preset, expected_type=type_hints["preset"])
            check_type(argname="argument theme", value=theme, expected_type=type_hints["theme"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "title": title,
        }
        if preset is not None:
            self._values["preset"] = preset
        if theme is not None:
            self._values["theme"] = theme

    @builtins.property
    def title(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def preset(
        self,
    ) -> typing.Optional[_aws_prototyping_sdk_cdk_graph_3c35d073.FilterPreset]:
        '''
        :stability: experimental
        '''
        result = self._values.get("preset")
        return typing.cast(typing.Optional[_aws_prototyping_sdk_cdk_graph_3c35d073.FilterPreset], result)

    @builtins.property
    def theme(
        self,
    ) -> typing.Optional[typing.Union["IGraphThemeConfigAlt", builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("theme")
        return typing.cast(typing.Optional[typing.Union["IGraphThemeConfigAlt", builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiagramOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@aws-prototyping-sdk/cdk-graph-plugin-diagram.GraphThemeRenderingIconTarget"
)
class GraphThemeRenderingIconTarget(enum.Enum):
    '''(experimental) Icon rendering target options for GraphTheme.

    :stability: experimental
    '''

    DATA = "DATA"
    '''(experimental) Data icon (eg: EC2 instance type icon, T2).

    Resolution precedence: ``data => resource => general => service => category``

    :stability: experimental
    '''
    RESOURCE = "RESOURCE"
    '''(experimental) Resource icon.

    Resolution precedence: ``resource => general => service => category``

    :stability: experimental
    '''
    GENERAL = "GENERAL"
    '''(experimental) General icon.

    Resolution precedence: ``resource => general => service => category``

    :stability: experimental
    '''
    SERVICE = "SERVICE"
    '''(experimental) Service icon.

    Resolution precedence: ``service => category``

    :stability: experimental
    '''
    CATEGORY = "CATEGORY"
    '''(experimental) Category icon.

    Resolution precedence: ``category``

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/cdk-graph-plugin-diagram.IDiagramConfigBase",
    jsii_struct_bases=[],
    name_mapping={"filter_plan": "filterPlan", "format": "format", "theme": "theme"},
)
class IDiagramConfigBase:
    def __init__(
        self,
        *,
        filter_plan: typing.Optional[_aws_prototyping_sdk_cdk_graph_3c35d073.IGraphFilterPlan] = None,
        format: typing.Optional[typing.Union[DiagramFormat, typing.Sequence[DiagramFormat]]] = None,
        theme: typing.Optional[typing.Union["IGraphThemeConfigAlt", builtins.str]] = None,
    ) -> None:
        '''(experimental) Base config to specific a unique diagram to be generated.

        :param filter_plan: (experimental) Graph {@link IGraphFilterPlanFilter Plan} used to generate a unique diagram.
        :param format: (experimental) The output format(s) to generated. Default: ``DiagramFormat.PNG`` - which will through extension also generate ``DiagramFormat.SVG`` and ``DiagramFormat.DOT``
        :param theme: (experimental) Config for graph theme.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb282e5d752c2da4a2f5bdc64f0187fcf747beee42328ca2d078d635d05ddea9)
            check_type(argname="argument filter_plan", value=filter_plan, expected_type=type_hints["filter_plan"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument theme", value=theme, expected_type=type_hints["theme"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if filter_plan is not None:
            self._values["filter_plan"] = filter_plan
        if format is not None:
            self._values["format"] = format
        if theme is not None:
            self._values["theme"] = theme

    @builtins.property
    def filter_plan(
        self,
    ) -> typing.Optional[_aws_prototyping_sdk_cdk_graph_3c35d073.IGraphFilterPlan]:
        '''(experimental) Graph {@link IGraphFilterPlanFilter Plan}  used to generate a unique diagram.

        :stability: experimental
        '''
        result = self._values.get("filter_plan")
        return typing.cast(typing.Optional[_aws_prototyping_sdk_cdk_graph_3c35d073.IGraphFilterPlan], result)

    @builtins.property
    def format(
        self,
    ) -> typing.Optional[typing.Union[DiagramFormat, typing.List[DiagramFormat]]]:
        '''(experimental) The output format(s) to generated.

        :default: ``DiagramFormat.PNG`` - which will through extension also generate ``DiagramFormat.SVG`` and ``DiagramFormat.DOT``

        :stability: experimental
        '''
        result = self._values.get("format")
        return typing.cast(typing.Optional[typing.Union[DiagramFormat, typing.List[DiagramFormat]]], result)

    @builtins.property
    def theme(
        self,
    ) -> typing.Optional[typing.Union["IGraphThemeConfigAlt", builtins.str]]:
        '''(experimental) Config for graph theme.

        :stability: experimental
        '''
        result = self._values.get("theme")
        return typing.cast(typing.Optional[typing.Union["IGraphThemeConfigAlt", builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IDiagramConfigBase(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(
    jsii_type="@aws-prototyping-sdk/cdk-graph-plugin-diagram.IGraphThemeConfigAlt"
)
class IGraphThemeConfigAlt(typing_extensions.Protocol):
    '''(experimental) GraphThemeConfigAlt is simplified definition of theme to apply.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="rendering")
    def rendering(self) -> typing.Optional["IGraphThemeRendering"]:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="theme")
    def theme(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        ...


class _IGraphThemeConfigAltProxy:
    '''(experimental) GraphThemeConfigAlt is simplified definition of theme to apply.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph-plugin-diagram.IGraphThemeConfigAlt"

    @builtins.property
    @jsii.member(jsii_name="rendering")
    def rendering(self) -> typing.Optional["IGraphThemeRendering"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional["IGraphThemeRendering"], jsii.get(self, "rendering"))

    @builtins.property
    @jsii.member(jsii_name="theme")
    def theme(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "theme"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGraphThemeConfigAlt).__jsii_proxy_class__ = lambda : _IGraphThemeConfigAltProxy


@jsii.interface(
    jsii_type="@aws-prototyping-sdk/cdk-graph-plugin-diagram.IGraphThemeRenderingIconProps"
)
class IGraphThemeRenderingIconProps(typing_extensions.Protocol):
    '''(experimental) Icon specific properties for configuring graph rendering of resource icons.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="cfnResourceIconMax")
    def cfn_resource_icon_max(self) -> typing.Optional[GraphThemeRenderingIconTarget]:
        '''(experimental) Highest Graph.CfnResourceNode icon to render.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="cfnResourceIconMin")
    def cfn_resource_icon_min(self) -> typing.Optional[GraphThemeRenderingIconTarget]:
        '''(experimental) Lowest Graph.CfnResourceNode icon to render.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="resourceIconMax")
    def resource_icon_max(self) -> typing.Optional[GraphThemeRenderingIconTarget]:
        '''(experimental) Highest Graph.ResourceNode icon to render.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="resourceIconMin")
    def resource_icon_min(self) -> typing.Optional[GraphThemeRenderingIconTarget]:
        '''(experimental) Lowest Graph.ResourceNode icon to render.

        :stability: experimental
        '''
        ...


class _IGraphThemeRenderingIconPropsProxy:
    '''(experimental) Icon specific properties for configuring graph rendering of resource icons.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph-plugin-diagram.IGraphThemeRenderingIconProps"

    @builtins.property
    @jsii.member(jsii_name="cfnResourceIconMax")
    def cfn_resource_icon_max(self) -> typing.Optional[GraphThemeRenderingIconTarget]:
        '''(experimental) Highest Graph.CfnResourceNode icon to render.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[GraphThemeRenderingIconTarget], jsii.get(self, "cfnResourceIconMax"))

    @builtins.property
    @jsii.member(jsii_name="cfnResourceIconMin")
    def cfn_resource_icon_min(self) -> typing.Optional[GraphThemeRenderingIconTarget]:
        '''(experimental) Lowest Graph.CfnResourceNode icon to render.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[GraphThemeRenderingIconTarget], jsii.get(self, "cfnResourceIconMin"))

    @builtins.property
    @jsii.member(jsii_name="resourceIconMax")
    def resource_icon_max(self) -> typing.Optional[GraphThemeRenderingIconTarget]:
        '''(experimental) Highest Graph.ResourceNode icon to render.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[GraphThemeRenderingIconTarget], jsii.get(self, "resourceIconMax"))

    @builtins.property
    @jsii.member(jsii_name="resourceIconMin")
    def resource_icon_min(self) -> typing.Optional[GraphThemeRenderingIconTarget]:
        '''(experimental) Lowest Graph.ResourceNode icon to render.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[GraphThemeRenderingIconTarget], jsii.get(self, "resourceIconMin"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGraphThemeRenderingIconProps).__jsii_proxy_class__ = lambda : _IGraphThemeRenderingIconPropsProxy


@jsii.interface(
    jsii_type="@aws-prototyping-sdk/cdk-graph-plugin-diagram.IGraphThemeRenderingOptions"
)
class IGraphThemeRenderingOptions(typing_extensions.Protocol):
    '''(experimental) Additional graph rendering options.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="layout")
    def layout(self) -> typing.Optional[builtins.str]:
        '''(experimental) Layout direction of the graph.

        :default: horizontal

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specify regex pattern to match root stacks to render.

        :default: undefined Will render all stacks

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="stage")
    def stage(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specify which stage to render when multiple stages are available.

        Can be a preset value of "first", "last", and "all", or regex string of the stage(s) to render.

        :default: last

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="unconstrainedCrossClusterEdges")
    def unconstrained_cross_cluster_edges(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Prevent cross-cluster edges from ranking nodes in layout.

        :default: false

        :see: https://graphviz.org/docs/attrs/constraint/
        :stability: experimental
        '''
        ...


class _IGraphThemeRenderingOptionsProxy:
    '''(experimental) Additional graph rendering options.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph-plugin-diagram.IGraphThemeRenderingOptions"

    @builtins.property
    @jsii.member(jsii_name="layout")
    def layout(self) -> typing.Optional[builtins.str]:
        '''(experimental) Layout direction of the graph.

        :default: horizontal

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "layout"))

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specify regex pattern to match root stacks to render.

        :default: undefined Will render all stacks

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stack"))

    @builtins.property
    @jsii.member(jsii_name="stage")
    def stage(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specify which stage to render when multiple stages are available.

        Can be a preset value of "first", "last", and "all", or regex string of the stage(s) to render.

        :default: last

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stage"))

    @builtins.property
    @jsii.member(jsii_name="unconstrainedCrossClusterEdges")
    def unconstrained_cross_cluster_edges(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Prevent cross-cluster edges from ranking nodes in layout.

        :default: false

        :see: https://graphviz.org/docs/attrs/constraint/
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "unconstrainedCrossClusterEdges"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGraphThemeRenderingOptions).__jsii_proxy_class__ = lambda : _IGraphThemeRenderingOptionsProxy


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/cdk-graph-plugin-diagram.IPluginConfig",
    jsii_struct_bases=[],
    name_mapping={"defaults": "defaults", "diagrams": "diagrams"},
)
class IPluginConfig:
    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Union[IDiagramConfigBase, typing.Dict[builtins.str, typing.Any]]] = None,
        diagrams: typing.Optional[typing.Sequence[typing.Union["IDiagramConfig", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Plugin configuration for diagram plugin.

        :param defaults: (experimental) Default configuration to apply to all diagrams.
        :param diagrams: (experimental) List of diagram configurations to generate diagrams.

        :stability: experimental
        '''
        if isinstance(defaults, dict):
            defaults = IDiagramConfigBase(**defaults)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3700f187e268cb7326cd34d07b633bd15a7c1b9a48636a05c797543469b73dbf)
            check_type(argname="argument defaults", value=defaults, expected_type=type_hints["defaults"])
            check_type(argname="argument diagrams", value=diagrams, expected_type=type_hints["diagrams"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if defaults is not None:
            self._values["defaults"] = defaults
        if diagrams is not None:
            self._values["diagrams"] = diagrams

    @builtins.property
    def defaults(self) -> typing.Optional[IDiagramConfigBase]:
        '''(experimental) Default configuration to apply to all diagrams.

        :stability: experimental
        '''
        result = self._values.get("defaults")
        return typing.cast(typing.Optional[IDiagramConfigBase], result)

    @builtins.property
    def diagrams(self) -> typing.Optional[typing.List["IDiagramConfig"]]:
        '''(experimental) List of diagram configurations to generate diagrams.

        :stability: experimental
        '''
        result = self._values.get("diagrams")
        return typing.cast(typing.Optional[typing.List["IDiagramConfig"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IPluginConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/cdk-graph-plugin-diagram.IDiagramConfig",
    jsii_struct_bases=[IDiagramConfigBase],
    name_mapping={
        "filter_plan": "filterPlan",
        "format": "format",
        "theme": "theme",
        "name": "name",
        "title": "title",
        "ignore_defaults": "ignoreDefaults",
    },
)
class IDiagramConfig(IDiagramConfigBase):
    def __init__(
        self,
        *,
        filter_plan: typing.Optional[_aws_prototyping_sdk_cdk_graph_3c35d073.IGraphFilterPlan] = None,
        format: typing.Optional[typing.Union[DiagramFormat, typing.Sequence[DiagramFormat]]] = None,
        theme: typing.Optional[typing.Union[IGraphThemeConfigAlt, builtins.str]] = None,
        name: builtins.str,
        title: builtins.str,
        ignore_defaults: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Diagram configuration definition.

        :param filter_plan: (experimental) Graph {@link IGraphFilterPlanFilter Plan} used to generate a unique diagram.
        :param format: (experimental) The output format(s) to generated. Default: ``DiagramFormat.PNG`` - which will through extension also generate ``DiagramFormat.SVG`` and ``DiagramFormat.DOT``
        :param theme: (experimental) Config for graph theme.
        :param name: (experimental) Name of the diagram. Used as the basename of the generated file(s) which gets the extension appended.
        :param title: (experimental) The title of the diagram.
        :param ignore_defaults: (experimental) Indicates if default diagram config is applied as defaults to this config. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87b4053fe8ec66bed0c46fa41ccfd65649ef3193496ddb29883a342b6cfffab7)
            check_type(argname="argument filter_plan", value=filter_plan, expected_type=type_hints["filter_plan"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument theme", value=theme, expected_type=type_hints["theme"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument ignore_defaults", value=ignore_defaults, expected_type=type_hints["ignore_defaults"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "title": title,
        }
        if filter_plan is not None:
            self._values["filter_plan"] = filter_plan
        if format is not None:
            self._values["format"] = format
        if theme is not None:
            self._values["theme"] = theme
        if ignore_defaults is not None:
            self._values["ignore_defaults"] = ignore_defaults

    @builtins.property
    def filter_plan(
        self,
    ) -> typing.Optional[_aws_prototyping_sdk_cdk_graph_3c35d073.IGraphFilterPlan]:
        '''(experimental) Graph {@link IGraphFilterPlanFilter Plan}  used to generate a unique diagram.

        :stability: experimental
        '''
        result = self._values.get("filter_plan")
        return typing.cast(typing.Optional[_aws_prototyping_sdk_cdk_graph_3c35d073.IGraphFilterPlan], result)

    @builtins.property
    def format(
        self,
    ) -> typing.Optional[typing.Union[DiagramFormat, typing.List[DiagramFormat]]]:
        '''(experimental) The output format(s) to generated.

        :default: ``DiagramFormat.PNG`` - which will through extension also generate ``DiagramFormat.SVG`` and ``DiagramFormat.DOT``

        :stability: experimental
        '''
        result = self._values.get("format")
        return typing.cast(typing.Optional[typing.Union[DiagramFormat, typing.List[DiagramFormat]]], result)

    @builtins.property
    def theme(
        self,
    ) -> typing.Optional[typing.Union[IGraphThemeConfigAlt, builtins.str]]:
        '''(experimental) Config for graph theme.

        :stability: experimental
        '''
        result = self._values.get("theme")
        return typing.cast(typing.Optional[typing.Union[IGraphThemeConfigAlt, builtins.str]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) Name of the diagram.

        Used as the basename of the generated file(s) which gets the extension appended.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''(experimental) The title of the diagram.

        :stability: experimental
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ignore_defaults(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates if default diagram config is applied as defaults to this config.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("ignore_defaults")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IDiagramConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(
    jsii_type="@aws-prototyping-sdk/cdk-graph-plugin-diagram.IGraphThemeRendering"
)
class IGraphThemeRendering(
    IGraphThemeRenderingIconProps,
    IGraphThemeRenderingOptions,
    typing_extensions.Protocol,
):
    '''(experimental) Properties for defining the rendering options for the graph theme.

    :stability: experimental
    '''

    pass


class _IGraphThemeRenderingProxy(
    jsii.proxy_for(IGraphThemeRenderingIconProps), # type: ignore[misc]
    jsii.proxy_for(IGraphThemeRenderingOptions), # type: ignore[misc]
):
    '''(experimental) Properties for defining the rendering options for the graph theme.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-prototyping-sdk/cdk-graph-plugin-diagram.IGraphThemeRendering"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGraphThemeRendering).__jsii_proxy_class__ = lambda : _IGraphThemeRenderingProxy


__all__ = [
    "CdkGraphDiagramPlugin",
    "DiagramFormat",
    "DiagramOptions",
    "GraphThemeRenderingIconTarget",
    "IDiagramConfig",
    "IDiagramConfigBase",
    "IGraphThemeConfigAlt",
    "IGraphThemeRendering",
    "IGraphThemeRenderingIconProps",
    "IGraphThemeRenderingOptions",
    "IPluginConfig",
]

publication.publish()

def _typecheckingstub__2c2c702aa641239e3944c5e390fa5500dfe4e2fb13fbc6f7273623914011bb78(
    name: builtins.str,
    format: DiagramFormat,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e705150c6494bb72a14eb56acfb819db5ab9d9a3a7abf142762746a723048619(
    name: builtins.str,
    format: DiagramFormat,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c465087309222b9a22cda02d8c3dcbdae9b128b2d0c03b955c47d91810c85edc(
    name: builtins.str,
    format: DiagramFormat,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd20e03a66d768d39dad86a2939fae03a0a2e870540db7c35a8d6f0624464fc6(
    value: _aws_prototyping_sdk_cdk_graph_3c35d073.IGraphPluginBindCallback,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb806c27af67b4d37164309b0a8a6b1ee2052cb809973708c60e38a73353d492(
    value: typing.Optional[_aws_prototyping_sdk_cdk_graph_3c35d073.IGraphReportCallback],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__872e0fa6b2a1dc9dfac4874b80a6fbc55e439af2940a0bfbcbf836b0916c1a86(
    *,
    title: builtins.str,
    preset: typing.Optional[_aws_prototyping_sdk_cdk_graph_3c35d073.FilterPreset] = None,
    theme: typing.Optional[typing.Union[IGraphThemeConfigAlt, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb282e5d752c2da4a2f5bdc64f0187fcf747beee42328ca2d078d635d05ddea9(
    *,
    filter_plan: typing.Optional[_aws_prototyping_sdk_cdk_graph_3c35d073.IGraphFilterPlan] = None,
    format: typing.Optional[typing.Union[DiagramFormat, typing.Sequence[DiagramFormat]]] = None,
    theme: typing.Optional[typing.Union[IGraphThemeConfigAlt, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3700f187e268cb7326cd34d07b633bd15a7c1b9a48636a05c797543469b73dbf(
    *,
    defaults: typing.Optional[typing.Union[IDiagramConfigBase, typing.Dict[builtins.str, typing.Any]]] = None,
    diagrams: typing.Optional[typing.Sequence[typing.Union[IDiagramConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87b4053fe8ec66bed0c46fa41ccfd65649ef3193496ddb29883a342b6cfffab7(
    *,
    filter_plan: typing.Optional[_aws_prototyping_sdk_cdk_graph_3c35d073.IGraphFilterPlan] = None,
    format: typing.Optional[typing.Union[DiagramFormat, typing.Sequence[DiagramFormat]]] = None,
    theme: typing.Optional[typing.Union[IGraphThemeConfigAlt, builtins.str]] = None,
    name: builtins.str,
    title: builtins.str,
    ignore_defaults: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass
