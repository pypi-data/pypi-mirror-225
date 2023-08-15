/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Interface Declarations                                                     *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace mlir {
namespace gpu {
class TargetAttrInterface;
namespace detail {
struct TargetAttrInterfaceInterfaceTraits {
  struct Concept {
    /// The methods defined by the interface.
    std::optional<SmallVector<char, 0>> (*serializeToObject)(const Concept *impl, ::mlir::Attribute , Operation*, const gpu::TargetOptions&);
  };
  template<typename ConcreteAttr>
  class Model : public Concept {
  public:
    using Interface = ::mlir::gpu::TargetAttrInterface;
    Model() : Concept{serializeToObject} {}

    static inline std::optional<SmallVector<char, 0>> serializeToObject(const Concept *impl, ::mlir::Attribute tablegen_opaque_val, Operation* module, const gpu::TargetOptions& options);
  };
  template<typename ConcreteAttr>
  class FallbackModel : public Concept {
  public:
    using Interface = ::mlir::gpu::TargetAttrInterface;
    FallbackModel() : Concept{serializeToObject} {}

    static inline std::optional<SmallVector<char, 0>> serializeToObject(const Concept *impl, ::mlir::Attribute tablegen_opaque_val, Operation* module, const gpu::TargetOptions& options);
  };
  template<typename ConcreteModel, typename ConcreteAttr>
  class ExternalModel : public FallbackModel<ConcreteModel> {
  public:
    using ConcreteEntity = ConcreteAttr;
  };
};template <typename ConcreteAttr>
struct TargetAttrInterfaceTrait;

} // namespace detail
class TargetAttrInterface : public ::mlir::AttributeInterface<TargetAttrInterface, detail::TargetAttrInterfaceInterfaceTraits> {
public:
  using ::mlir::AttributeInterface<TargetAttrInterface, detail::TargetAttrInterfaceInterfaceTraits>::AttributeInterface;
  template <typename ConcreteAttr>
  struct Trait : public detail::TargetAttrInterfaceTrait<ConcreteAttr> {};
  /// Serializes a GPU module to a string containing a representation of the
  /// module.
  /// 
  /// If serialization fails then the method should return `std::nullopt`.
  /// 
  /// The `module` argument must be a GPU Module Op. The `options` argument is
  /// meant to be used for passing additional options that are not in the
  /// attribute.
  std::optional<SmallVector<char, 0>> serializeToObject(Operation* module, const gpu::TargetOptions& options) const;
};
namespace detail {
  template <typename ConcreteAttr>
  struct TargetAttrInterfaceTrait : public ::mlir::AttributeInterface<TargetAttrInterface, detail::TargetAttrInterfaceInterfaceTraits>::Trait<ConcreteAttr> {
  };
}// namespace detail
} // namespace gpu
} // namespace mlir
namespace mlir {
namespace gpu {
template<typename ConcreteAttr>
std::optional<SmallVector<char, 0>> detail::TargetAttrInterfaceInterfaceTraits::Model<ConcreteAttr>::serializeToObject(const Concept *impl, ::mlir::Attribute tablegen_opaque_val, Operation* module, const gpu::TargetOptions& options) {
  return (::llvm::cast<ConcreteAttr>(tablegen_opaque_val)).serializeToObject(module, options);
}
template<typename ConcreteAttr>
std::optional<SmallVector<char, 0>> detail::TargetAttrInterfaceInterfaceTraits::FallbackModel<ConcreteAttr>::serializeToObject(const Concept *impl, ::mlir::Attribute tablegen_opaque_val, Operation* module, const gpu::TargetOptions& options) {
  return static_cast<const ConcreteAttr *>(impl)->serializeToObject(tablegen_opaque_val, module, options);
}
} // namespace gpu
} // namespace mlir
