#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

%define 	module	traitlets
Summary:	A configuration system for Python applications
Summary(pl.UTF-8):	System konfiguracji dla aplikacji w Pythonie
Name:		python3-%{module}
Version:	5.14.3
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://github.com/ipython/traitlets/releases
Source0:	https://github.com/ipython/traitlets/releases/download/v%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	f6e6529cca4cbe3299e3f07ce24d3fdc
URL:		https://traitlets.readthedocs.io/en/stable/
%if %(locale -a | grep -q '^C\.utf8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
BuildRequires:	python3-build
BuildRequires:	python3-hatchling >= 1.5
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.8
%if %{with tests}
BuildRequires:	python3-decorator
BuildRequires:	python3-ipython_genutils
BuildRequires:	python3-pytest
BuildRequires:	python3-six
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-ipython_genutils
BuildRequires:	python3-myst_parser
BuildRequires:	python3-pydata_sphinx_theme
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.8
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

%{__sed} -i -e '1s,/usr/bin/env python$,%{__python3},' \
	examples/{argcomplete_app.py,myapp.py,subcommands_app.py}

%build
%py3_build_pyproject

%if %{with tests}
%{__python3} -m pytest traitlets
%endif

%if %{with doc}
PYTHONPATH="$(pwd)" \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT
%py3_install_pyproject

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/traitlets/tests

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -p examples/*.py $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%{py3_sitescriptdir}/traitlets
%{py3_sitescriptdir}/traitlets-%{version}.dist-info
%{_examplesdir}/python3-%{module}-%{version}

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,*.html,*.js}
%endif
