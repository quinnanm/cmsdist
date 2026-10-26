### RPM external alkaid 0.8.2
## INCLUDE compilation_flags
## INCLUDE cpp-standard
# Only the C++ runtime of alkaid (the ALIR interpreter in src/alkaid/_binary/alir, Apache-2.0 dual licensed since
# v0.8.2): it evaluates alkaid model files (*.json / *.json.gz) bit-exactly, for the Phase-2 L1 NN emulators in
# L1Trigger/Phase2L1ParticleFlow. The Python package and its nanobind bindings are not built.
Source: https://github.com/calad0i/%{n}/archive/refs/tags/v%{realversion}.tar.gz
Requires: json zlib

%prep
%setup -n %{n}-%{realversion}

%build
cd src/alkaid/_binary/alir
# -fopenmp-simd: the kernels' "#pragma omp simd" vectorize without any OpenMP runtime (nothing links libgomp).
for f in ALIRInterpreter_load ALIRInterpreter_load_json ALIRInterpreter_transpile ALIRInterpreter_dispatch; do
  ${CXX:-g++} -std=c++%{cms_cxx_standard} -O3 -fPIC -fopenmp-simd %{?arch_build_flags} \
    -I${JSON_ROOT}/include -I${ZLIB_ROOT}/include -c ${f}.cc -o ${f}.o
done
${CXX:-g++} -shared -o libalkaid_alir.so ALIRInterpreter_*.o -L${ZLIB_ROOT}/lib -lz

%install
mkdir -p %{i}/lib %{i}/include/alkaid/alir
cp src/alkaid/_binary/alir/libalkaid_alir.so %{i}/lib/
# Headers under alkaid/alir/: #include "alkaid/alir/ALIRInterpreter.hh"
cp src/alkaid/_binary/alir/*.hh src/alkaid/_binary/alir/LICENSE %{i}/include/alkaid/alir/
