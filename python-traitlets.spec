#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	traitlets
Summary:	A configuration system for Python applications
Summary(pl.UTF-8):	System konfiguracji dla aplikacji w Pythonie
Name:		python-%{module}
Version:	4.3.2
Release:	5
License:	BSD
Group:		Libraries/Python
#Source0Download: https://github.com/ipython/traitlets/releases
# TODO:		https://github.com/ipython/traitlets/archive/%{version}/%{module}-%{version}.tar.gz
Source0:	https://github.com/ipython/traitlets/archive/%{version}.tar.gz
# Source0-md5:	0b5b7986aef676d12f31a16cbbe3ed92
Patch0:		%{name}-use-setuptools.patch
URL:		https://traitlets.readthedocs.io/en/stable/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-decorator
BuildRequires:	python-enum34
BuildRequires:	python-ipython_genutils
BuildRequires:	python-mock
BuildRequires:	python-pytest
BuildRequires:	python-six
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.3
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-decorator
%if "%{py3_ver}" < "3.4"
BuildRequires:	python3-enum34
%endif
BuildRequires:	python3-ipython_genutils
BuildRequires:	python3-pytest
BuildRequires:	python3-six
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-ipython_genutils
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Traitlets is a framework that lets Python classes have attributes with
type checking, dynamically calculated default values, and "on change"
callbacks.

%description -l pl.UTF-8
Traitlets to szkielet pozwalający klasom Pythona na trzymanie
atrybutów ze sprawdzaniem typów, dynamicznie wyliczanymi wartościami
domyślnymi oraz wywołaniami wstecznym "przy zmianie".

%package -n python3-%{module}
Summary:	A configuration system for Python applications
Summary(pl.UTF-8):	System konfiguracji dla aplikacji w Pythonie
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.3

%description -n python3-%{module}
Traitlets is a framework that lets Python classes have attributes with
type checking, dynamically calculated default values, and "on change"
callbacks.

%description -n python3-%{module} -l pl.UTF-8
Traitlets to szkielet pozwalający klasom Pythona na trzymanie
atrybutów ze sprawdzaniem typów, dynamicznie wyliczanymi wartościami
domyślnymi oraz wywołaniami wstecznym "przy zmianie".

%package apidocs
Summary:	API documentation for traitlets module
Summary(pl.UTF-8):	Dokumentacja API modułu traitlets
Group:		Documentation

%description apidocs
API documentation for traitlets module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu traitlets.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1

%build
%if %{with python2}
%py_build

%if %{with tests}
%{__python} -m pytest traitlets
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
%{__python3} -m pytest traitlets
%endif
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/traitlets/{tests,config/tests,utils/tests}

install -d $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version}
cp -p examples/*.py $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version}
%endif

%if %{with python3}
%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/traitlets/{tests,config/tests,utils/tests}

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -p examples/*.py $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc COPYING.md README.md
%{py_sitescriptdir}/traitlets
%{py_sitescriptdir}/traitlets-%{version}-py*.egg-info
%{_examplesdir}/python-%{module}-%{version}
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc COPYING.md README.md
%{py3_sitescriptdir}/traitlets
%{py3_sitescriptdir}/traitlets-%{version}-py*.egg-info
%{_examplesdir}/python3-%{module}-%{version}
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,*.html,*.js}
%endif
