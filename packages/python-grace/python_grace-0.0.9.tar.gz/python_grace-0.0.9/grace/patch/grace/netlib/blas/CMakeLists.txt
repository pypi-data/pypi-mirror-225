add_library(
  blas
  daxpy.f
  ddot.f
  dgemv.f
  dger.f
  dnrm2.f
  dscal.f
  dspmv.f
  dspr2.f
  dswap.f
  lsame.f
  xerbla.f)
install(TARGETS blas ARCHIVE DESTINATION lib)
