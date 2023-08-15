/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Interface Definitions                                                      *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

/// Serializes a GPU module to a string containing a representation of the
/// module.
/// 
/// If serialization fails then the method should return `std::nullopt`.
/// 
/// The `module` argument must be a GPU Module Op. The `options` argument is
/// meant to be used for passing additional options that are not in the
/// attribute.
std::optional<SmallVector<char, 0>> mlir::gpu::TargetAttrInterface::serializeToObject(Operation* module, const gpu::TargetOptions& options) const {
      return getImpl()->serializeToObject(getImpl(), *this, module, options);
  }
