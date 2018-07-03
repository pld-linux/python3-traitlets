# TODO:
# - fix docs
# Conditional build:
%bcond_with	doc	# don't build doc
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

# NOTE: 'module' should match the python import path, not the egg name
%define 	module	traitlets
Summary:	A configuration system for Python applications
Summary(pl.UTF-8):	System konfiguracji dla aplikacji w Pythonie.
Name:		python-%{module}
Version:	4.3.2
Release:	3
License:	BSD
Group:		Libraries/Python
Source0:	https://github.com/ipython/traitlets/archive/%{version}.tar.gz
# Source0-md5:	0b5b7986aef676d12f31a16cbbe3ed92
URL:		https://traitlets.readthedocs.io/en/stable/
BuildRequires:	rpm-pythonprov
# for the py_build, py_install macros
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules
BuildRequires:	python-setuptools
BuildRequires:	python-sphinx_rtd_theme
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
BuildRequires:	python3-sphinx_rtd_theme

%endif
# when using /usr/bin/env or other in-place substitutions
#BuildRequires:	sed >= 4.0
# replace with other requires if defined in setup.py
Requires:	python-decorator
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Traitlets is a framework that lets Python classes have attributes with
type checking, dynamically calculated default values, and ‘on change’
callbacks.

%description -l pl.UTF-8
System konfiguracji dla aplikacji w Pythonie.

%package -n python3-%{module}
Summary:	-
Summary(pl.UTF-8):	-
Group:		Libraries/Python
Requires:	python3-decorator
Requires:	python3-modules

%description -n python3-%{module}

%description -n python3-%{module} -l pl.UTF-8

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}

#%{__sed} -i -e '1s,^#!.*python,#!%{__python},' %{name}.py

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

# in case there are examples provided
%if %{with python2}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python}|'
%endif
%if %{with python3}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python3}|'
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.md
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%{_examplesdir}/python-%{module}-%{version}
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README.md
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%{_examplesdir}/python3-%{module}-%{version}
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
