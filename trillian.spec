%global with_devel 0
%global with_bundled 1
%global with_check 0
%global with_unit_test 0

%global with_debug 0

%if 0%{?with_debug}
%global _find_debuginfo_dwz_opts %{nil}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package %{nil}
%endif

%if ! 0%{?gobuild:1}
%define gobuild(o:) GO111MODULE=off go build -buildmode pie -compiler gc -tags="rpm_crashtraceback ${BUILDTAGS:-}" -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n') -extldflags '-Wl,-z,relro -Wl,-z,now -specs=/usr/lib/rpm/redhat/redhat-hardened-ld '" -a -v -x %{?**};
%endif

%global provider github
%global provider_tld com
%global project google
%global repo %{name}
%global import_path %{provider}.%{provider_tld}/%{project}/%{repo}
%global git0 https://%{import_path}

Name: trillian
Version: 1.3.13
Release: 4%{?dist}
Summary: A transparent, highly scalable and cryptographically verifiable data store
License: ASL 2.0
URL: https://%{name}.io/
Source0: %{git0}/archive/v%{version}.tar.gz
BuildRequires: gcc
BuildRequires: golang
BuildRequires: glib2-devel
BuildRequires: glibc-devel
BuildRequires: glibc-static
BuildRequires: git-core
Requires: mariadb-server

%description
%{summry}

%prep
%autosetup -Sgit_am -n %{name}-%{version}

%build
export CGO_CFLAGS='-O2 -g -grecord-gcc-switches -pipe -Wall -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1 -ffat-lto-objects -fexceptions -fasynchronous-unwind-tables -fstack-protector-strong -fstack-clash-protection -D_GNU_SOURCE -D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64'
%ifarch x86_64
export CGO_CFLAGS="$CGO_CFLAGS -m64 -mtune=generic"
%if 0%{?fedora} || 0%{?centos} >= 8
export CGO_CFLAGS="$CGO_CFLAGS -fcf-protection"
%endif
%endif

mkdir bin
go build -o bin/%{name}_log_server ./cmd/%{name}_log_server
go build -o bin/%{name}_log_signer ./cmd/%{name}_log_signer

%install
install -dp %{buildroot}%{_bindir}
install -p bin/* %{buildroot}%{_bindir}

%check

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license LICENSE
%doc AUTHORS CHANGELOG.md CODEOWNERS CONTRIBUTING.md CONTRIBUTORS PULL_REQUEST_TEMPLATE.md README.md
%{_bindir}/%{name}_log_server
%{_bindir}/%{name}_log_signer

%changelog
* Tue May 18 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.3.13-4
- correct build steps for binaries

* Tue May 18 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.3.13-3
- requires: mariadb-server

* Tue May 18 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.3.13-2
- only install log_server and log_signer

* Tue May 18 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.3.13-1
- initial package
