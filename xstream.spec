# Copyright (c) 2000-2008, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define gcj_support 1

# If you don't want to build with maven, and use straight ant instead,
# give rpmbuild option '--without maven'
%define _without_maven 1
%define with_maven %{!?_without_maven:1}%{?_without_maven:0}
%define without_maven %{?_without_maven:1}%{!?_without_maven:0}

%define section   free

Name:           xstream
Version:        1.3
Release:        %mkrel 2.0.1
Epoch:          0
Summary:        XML serialization library

Group:          Development/Java
License:        BSD-Style
URL:            http://xstream.codehaus.org/
Source0:        http://repository.codehaus.org/com/thoughtworks/xstream/xstream-distribution/1.2.2/xstream-distribution-1.3-src.zip
Source1:        %{name}-settings.xml
Source2:        %{name}-jpp-depmap.xml

Patch0:         xstream-build_xml.patch
Patch1:         xstream-pom_xml.patch
Patch2:         xstream-xstream-pom_xml.patch
Patch3:         xstream-xstream-distribution-pom_xml.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

Requires(post):    jpackage-utils >= 0:1.7.2
Requires(postun):  jpackage-utils >= 0:1.7.2

%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel
%endif

%if ! %{gcj_support}
BuildArch:      noarch
%endif

BuildRequires:  java-devel = 0:1.5.0
BuildRequires:  jpackage-utils >= 0:1.7.4
BuildRequires:  ant >= 0:1.6.5
BuildRequires:  ant-junit
BuildRequires:  ant-trax
BuildRequires:  junit >= 0:3.8.1
%if %{with_maven}
BuildRequires:  maven2 >= 2.0.4-10jpp
BuildRequires:  maven2-plugin-antrun
BuildRequires:  maven2-plugin-compiler
BuildRequires:  maven2-plugin-dependency
BuildRequires:  maven2-plugin-install
BuildRequires:  maven2-plugin-jar
BuildRequires:  maven2-plugin-javadoc
BuildRequires:  maven2-plugin-release
BuildRequires:  maven2-plugin-resources
BuildRequires:  maven2-plugin-source
BuildRequires:  maven2-plugin-surefire
BuildRequires:  jakarta-slide-webdavclient
BuildRequires:  xsite
%endif
BuildRequires:  bea-stax >= 0:1.2.0
BuildRequires:  bea-stax-api >= 0:1.0.1
BuildRequires:  cglib >= 0:2.1.3
BuildRequires:  dom4j >= 0:1.6.1
BuildRequires:  jakarta-commons-lang >= 0:2.1
BuildRequires:  jakarta-oro >= 0:2.0.8
BuildRequires:  jdom >= 0:1.0
BuildRequires:  jettison >= 0:1.0
BuildRequires:  jmock >= 0:1.0.1
BuildRequires:  joda-time >= 0:1.2.1
BuildRequires:  wstx >= 0:3.2.0
BuildRequires:  xalan-j2 >= 0:2.7.0
BuildRequires:  xom >= 0:1.0
BuildRequires:  xpp3 >= 0:1.1.3.4

Requires:  bea-stax-api
Requires:  cglib
Requires:  dom4j
Requires:  jakarta-commons-lang
Requires:  jakarta-oro
Requires:  jdom
Requires:  jettison
Requires:  joda-time
Requires:  wstx
Requires:  xom
Requires:  xpp3

Requires(post):    jpackage-utils >= 0:1.7.4
Requires(postun):  jpackage-utils >= 0:1.7.4


%description
XStream is a simple library to serialize objects to XML 
and back again. A high level facade is supplied that 
simplifies common use cases. Custom objects can be serialized 
without need for specifying mappings. Speed and low memory 
footprint are a crucial part of the design, making it suitable 
for large object graphs or systems with high message throughput. 
No information is duplicated that can be obtained via reflection. 
This results in XML that is easier to read for humans and more 
compact than native Java serialization. XStream serializes internal 
fields, including private and final. Supports non-public and inner 
classes. Classes are not required to have default constructor. 
Duplicate references encountered in the object-model will be 
maintained. Supports circular references. By implementing an 
interface, XStream can serialize directly to/from any tree 
structure (not just XML). Strategies can be registered allowing 
customization of how particular types are represented as XML. 
When an exception occurs due to malformed XML, detailed diagnostics 
are provided to help isolate and fix the problem.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description    javadoc
%{summary}.

%if %{with_maven}
%package        manual
Summary:        Documents for %{name}
Group:          Development/Java

%description    manual
%{summary}.
%endif

%prep
%setup -q %{name}-%{version}
%remove_java_binaries
cp %{SOURCE1} settings.xml

#%patch0 -b .sav0
#%patch1 -b .sav1
#%patch2 -b .sav2
#%patch3 -b .sav3

# This test requires megginson's sax2
rm xstream/src/test/com/thoughtworks/xstream/io/xml/SaxWriterTest.java
# These sources are for Java5
# Keep them now
#rm -rf xstream/src/java/com/thoughtworks/xstream/annotations/
#rm -rf xstream/src/test/com/thoughtworks/acceptance/annotations/

mkdir -p xstream-distribution/target/xsite

%build
%if %{with_maven}
sed -i -e "s|<url>__JPP_URL_PLACEHOLDER__</url>|<url>file://`pwd`/.m2/repository</url>|g" settings.xml
sed -i -e "s|<url>__JAVADIR_PLACEHOLDER__</url>|<url>file://`pwd`/external_repo</url>|g" settings.xml
sed -i -e "s|<url>__MAVENREPO_DIR_PLACEHOLDER__</url>|<url>file://`pwd`/.m2/repository</url>|g" settings.xml
sed -i -e "s|<url>__MAVENDIR_PLUGIN_PLACEHOLDER__</url>|<url>file:///usr/share/maven2/plugins</url>|g" settings.xml
sed -i -e "s|<url>__ECLIPSEDIR_PLUGIN_PLACEHOLDER__</url>|<url>file:///usr/share/eclipse/plugins</url>|g" settings.xml

export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

mkdir external_repo
ln -s %{_javadir} external_repo/JPP

mvn-jpp \
        -e \
        -s $(pwd)/settings.xml \
        -Dmaven2.jpp.mode=true \
        -Dmaven.test.skip=true \
        -Dmaven2.jpp.depmap.file=%{SOURCE2} \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        install javadoc:javadoc \
        -P jdk16

%else
cd xstream
pushd lib
# cglib-nodep-2.1_3.jar.no
ln -sf $(build-classpath cglib-nodep)
# commons-lang-2.1.jar.no
ln -sf $(build-classpath commons-lang)
# dom4j-1.6.1.jar.no
ln -sf $(build-classpath dom4j)
# jdom-1.0.jar.no
ln -sf $(build-classpath jdom)
# jettison-1.0-RC1.jar.no
ln -sf $(build-classpath jettison)
# jmock-1.0.1.jar.no
ln -sf $(build-classpath jmock)
# joda-time-1.2.1.jar.no
ln -sf $(build-classpath joda-time)
# junit-3.8.1.jar.no
ln -sf $(build-classpath junit)
# oro-2.0.8.jar.no
ln -sf $(build-classpath oro)
# stax-1.2.0.jar.no
ln -sf $(build-classpath bea-stax-ri)
# stax-api-1.0.1.jar.no
ln -sf $(build-classpath bea-stax-api)
# wstx-asl-3.2.0.jar.no
ln -sf $(build-classpath wstx/wstx-asl)
# xml-writer-0.2.jar.no

#xom-1.1.jar.no
ln -sf $(build-classpath xom)
# xpp3_min-1.1.3.4.O.jar.no
ln -sf $(build-classpath xpp3)
popd
ant library javadoc
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -Dpm 644 xstream/target/%{name}-SNAPSHOT.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
%if %{with_maven}
install -Dpm 644 xstream-benchmark/target/%{name}-benchmark-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-benchmark-%{version}.jar
%else
install -Dpm 644 xstream/target/%{name}-benchmark-SNAPSHOT.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-benchmark-%{version}.jar
%endif

%add_to_maven_depmap com.thoughtworks.xstream xstream %{version} JPP %{name}
%add_to_maven_depmap com.thoughtworks.xstream xstream-benchmark %{version} JPP %{name}-benchmark
%add_to_maven_depmap com.thoughtworks.xstream xstream-parent %{version} JPP %{name}-parent

%create_jar_links

# poms
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -pm 644 pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-parent.pom
install -pm 644 xstream/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}.pom
install -pm 644 xstream-benchmark/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-benchmark.pom

#
install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/core
%if %{with_maven}
cp -pr xstream/target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/core
%else
cp -pr xstream/target/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/core
%endif
install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/benchmark
%if %{with_maven}
cp -pr xstream-benchmark/target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/benchmark
%else
cp -pr xstream/target/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/benchmark
%endif
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} 

# manual
install -dm 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/xsite
cp LICENSE.txt $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
%if %{with_maven}
rm -rf xstream-distribution/target/xsite/javadoc 
cp -pr xstream-distribution/target/xsite/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/xsite
%endif

%gcj_compile

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap
%if %{gcj_support}
%{update_gcjdb}
%endif

%postun
%update_maven_depmap 
%if %{gcj_support}
%{clean_gcjdb}
%endif

%files
%defattr(-,root,root,-)
%{_docdir}/%{name}-%{version}/LICENSE.txt
%{_javadir}/*.jar
%{_datadir}/maven2/poms/*
%{_mavendepmapfragdir}
%gcj_files

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%if %{with_maven}
%files manual
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}-%{version}/xsite
%endif
