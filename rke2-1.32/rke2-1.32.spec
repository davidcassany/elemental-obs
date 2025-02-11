#
# spec file for package rke2-1.32
#
# Copyright (c) 2025 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#

%define k8s_version 1.32.1
%define binary_name rke2

%define go_arch amd64
%ifarch aarch64
%define go_arch arm64
%endif

Name:           rke2-1.32
Version:        %{k8s_version}+rke2r1
Release:        0
Summary:        Rancher Kubernetes Engine
License:        Apache-2.0
URL:            https://github.com/rancher/rke2
Source0:        rke2-%{k8s_version}-%{go_arch}.tar.gz

%description
RKE2, also known as RKE Government, is Rancher's next-generation Kubernetes distribution

%prep
tar xzvf %{SOURCE0}

%install
# Install the binary.
install -D -m 0755 bin/%{binary_name} %{buildroot}/%{_bindir}/%{binary_name}

# systemd unit and env files
install -D -m 0644 lib/systemd/system/rke2-agent.service %{buildroot}/%{_unitdir}/rke2-agent.service
install -D -m 0644 lib/systemd/system/rke2-agent.env %{buildroot}/%{_unitdir}/rke2-agent.env
install -D -m 0644 lib/systemd/system/rke2-server.service %{buildroot}/%{_unitdir}/rke2-server.service
install -D -m 0644 lib/systemd/system/rke2-server.env %{buildroot}/%{_unitdir}/rke2-server.env

# configuration directory
install -d -m 0755 %{buildroot}/%{_sysconfdir}/cni/
install -d -m 0755 %{buildroot}/%{_sysconfdir}/cni/net.d/
install -d -m 0755 %{buildroot}/%{_sysconfdir}/rancher/
install -d -m 0755 %{buildroot}/%{_sysconfdir}/rancher/node/
install -d -m 0755 %{buildroot}/%{_sysconfdir}/rancher/%{binary_name}/
install -d -m 0750 %{buildroot}/%{_sharedstatedir}/kubelet/
install -d -m 0755 %{buildroot}/%{_sharedstatedir}/rancher/
install -d -m 0755 %{buildroot}/%{_sharedstatedir}/rancher/%{binary_name}/
install -d -m 0755 %{buildroot}/%{_localstatedir}/log/containers/
install -d -m 0755 %{buildroot}/%{_localstatedir}/log/pods/

%pre
%service_add_pre rke2-agent.service
%service_add_pre rke2-server.service

%post
%service_add_post rke2-agent.service
%service_add_post rke2-server.service

%preun
%service_del_preun rke2-agent.service
%service_del_preun rke2-server.service

%postun
%service_del_postun rke2-agent.service
%service_del_postun rke2-server.service

%files
%{_bindir}/%{binary_name}
%{_unitdir}/%{binary_name}-agent.env
%{_unitdir}/%{binary_name}-agent.service
%{_unitdir}/%{binary_name}-server.env
%{_unitdir}/%{binary_name}-server.service
%dir %config %{_sysconfdir}/cni/
%dir %config %{_sysconfdir}/cni/net.d/
%dir %config %{_sysconfdir}/rancher/
%dir %config %{_sysconfdir}/rancher/node/
%dir %config %{_sysconfdir}/rancher/rke2/
%dir %attr(750,root,root) %{_sharedstatedir}/kubelet/
%dir %{_sharedstatedir}/rancher/
%dir %{_sharedstatedir}/rancher/rke2/
%dir %{_localstatedir}/log/containers/
%dir %{_localstatedir}/log/pods/

%changelog
