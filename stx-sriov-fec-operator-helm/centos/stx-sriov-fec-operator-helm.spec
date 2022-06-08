# Application tunables (maps to metadata)
%global app_name sriov-fec-operator
%global helm_repo stx-platform

# Install location
%global app_folder /usr/local/share/applications/helm

# Build variables
%global helm_folder /usr/lib/helm

Summary: StarlingX Sriov Fec Operator Helm Charts
Name: stx-sriov-fec-operator-helm
Version: 1.0
Release: %{tis_patch_ver}%{?_tis_dist}
License: Apache-2.0
Group: base
Packager: Intel
URL: unknown

Source0: %{name}-%{version}.tar.gz

BuildArch: noarch

BuildRequires: helm
BuildRequires: python-k8sapp-sriov-fec-operator
BuildRequires: python-k8sapp-sriov-fec-operator-wheels

%description
StarlingX Sriov Fec Operator Helm Charts

%package fluxcd
Summary: StarlingX Sriov Fec Operator Application FluxCD Helm Charts
Group: base
License: Apache-2.0

%description fluxcd
StarlingX Sriov Fec Operator Application FluxCD Helm Charts

%prep
%setup -n %{name}-%{version}

%build
# This chart does not require chartmuseum server since
# it has no dependency on local or stable repos.
# Make the charts. These produce a tgz file
cd helm-charts
make sriov-fec-operator

# switch back to source root
cd -


# Create a chart tarball compliant with sysinv kube-app.py
%define app_staging %{_builddir}/staging
%define app_tarball_fluxcd %{app_name}-%{version}-%{tis_patch_ver}.tgz
%define app_path %{_builddir}/%{app_tarball_fluxcd}

# Setup staging
cd %{_builddir}/%{name}-%{version}
mkdir -p %{app_staging}
cp files/metadata.yaml %{app_staging}
cp -R fluxcd-manifests %{app_staging}/
mkdir -p %{app_staging}/charts
cp helm-charts/*.tgz %{app_staging}/charts

# Copy the plugins: installed in the buildroot
mkdir -p %{app_staging}/plugins
cp /plugins/%{app_name}/*.whl %{app_staging}/plugins

cd %{app_staging}

# Populate metadata
sed -i 's/@APP_NAME@/%{app_name}/g' %{app_staging}/metadata.yaml
sed -i 's/@APP_VERSION@/%{version}-%{tis_patch_ver}/g' %{app_staging}/metadata.yaml
sed -i 's/@HELM_REPO@/%{helm_repo}/g' %{app_staging}/metadata.yaml

# calculate checksum of all files in app_staging
find . -type f ! -name '*.md5' -print0 | xargs -0 md5sum > checksum.md5
# package the app
tar -zcf %{app_path} -C %{app_staging}/ .

# switch back to source root
cd -

# Cleanup staging
rm -fr %{app_staging}

%install
install -d -m 755 %{buildroot}/%{app_folder}
install -p -D -m 755 %{app_path} %{buildroot}/%{app_folder}

%files
%defattr(-,root,root,-)
%{app_folder}/%{app_tarball_fluxcd}
