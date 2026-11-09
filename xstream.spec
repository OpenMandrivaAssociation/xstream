Name:		xstream
Version:	1.4.21
Release:	1
Summary:	Java object to XML serialization
Group:		Development/Java
License:	BSD
URL:		https://x-stream.github.io/
Source0:	https://github.com/x-stream/xstream/archive/refs/tags/XSTREAM_%(echo %{version} | tr . _).tar.gz#/xstream-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	java-current-devel
BuildRequires:	sysjar
BuildRequires:	mvn(xmlpull:xmlpull)
BuildRequires:	mvn(io.github.x-stream:mxparser)
BuildRequires:	mvn(org.jdom:jdom2)
BuildRequires:	mvn(org.dom4j:dom4j)
BuildRequires:	mvn(joda-time:joda-time)
BuildRequires:	mvn(org.codehaus.jettison:jettison)
BuildRequires:	mvn(javax.xml.bind:jaxb-api)
BuildRequires:	mvn(javax.activation:activation)

%description
XStream serializes Java objects to XML and back. Groovy 3.0.22 calls
XStream(StaxDriver) from XStreamUtils when groovy.ast=xml, and the
no-arg constructor uses an XmlPull driver. Gradle's default
distribution is that Groovy. 1.4.21 fixes CVE-2024-47072, a stack
overflow in BinaryDriver, and adds a WeakHashMap converter that does
not touch the ReentrantLock added in Java 19.

The Hibernate and JMH modules are not built. Drivers for libraries
cooker does not ship are left out: xpp3, kxml2, JDOM 1, XOM, CGLIB,
Woodstox, and the BEA StAX driver. The sun.misc.Unsafe reflection
providers are left out because a --release 8 compile cannot see that
package. PureJavaReflectionProvider remains.

%prep
%autosetup -n xstream-XSTREAM_%(echo %{version} | tr . _)

%build
export JAVA_HOME=%{_jvmdir}/java-openjdk
export PATH=$JAVA_HOME/bin:$PATH
find xstream/src/java -name '*.java' | grep -v -E \
	'/(BEAStaxDriver|WstxDriver|Xpp3Driver|Xpp3DomDriver|Xpp3DomBuilder|KXml2Driver|KXml2DomDriver|JDomDriver|JDomReader|JDomWriter|XomDriver|XomReader|XomWriter|CGLIBEnhancedConverter|CGLIBMapper|CGLIBProxyTypePermission|SunLimitedUnsafeReflectionProvider|SunUnsafeReflectionProvider|Sun14ReflectionProvider)\.java$' \
	> sources.list
mkdir -p classes
javac --release 8 -encoding UTF-8 -Xlint:-options \
	-cp %{_javadir}/xmlpull.jar:%{_javadir}/mxparser.jar:%{_javadir}/jdom2/jdom2.jar:%{_javadir}/dom4j.jar:%{_javadir}/joda-time.jar:%{_javadir}/jettison.jar:%{_javadir}/javax.xml.bind.jar:%{_javadir}/javax.activation.jar \
	-d classes @sources.list
jar cf %{name}.jar -C classes .
cat > %{name}.pom <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.thoughtworks.xstream</groupId>
  <artifactId>xstream</artifactId>
  <version>%{version}</version>
  <name>XStream Core</name>
  <description>Serialize Java objects to XML. Links the system MXParser.</description>
  <url>https://x-stream.github.io/</url>
  <licenses>
    <license>
      <name>BSD-3-Clause</name>
      <url>https://raw.githubusercontent.com/x-stream/xstream/XSTREAM_1_4_21/LICENSE.txt</url>
    </license>
  </licenses>
  <dependencies>
    <dependency>
      <groupId>io.github.x-stream</groupId>
      <artifactId>mxparser</artifactId>
      <version>1.2.3</version>
    </dependency>
    <dependency>
      <groupId>xmlpull</groupId>
      <artifactId>xmlpull</artifactId>
      <version>1.1.3.4c</version>
    </dependency>
    <dependency>
      <groupId>org.jdom</groupId>
      <artifactId>jdom2</artifactId>
      <version>2.0.6.1</version>
      <optional>true</optional>
    </dependency>
    <dependency>
      <groupId>org.dom4j</groupId>
      <artifactId>dom4j</artifactId>
      <version>2.2.0</version>
      <optional>true</optional>
    </dependency>
    <dependency>
      <groupId>joda-time</groupId>
      <artifactId>joda-time</artifactId>
      <version>2.15.1</version>
      <optional>true</optional>
    </dependency>
    <dependency>
      <groupId>org.codehaus.jettison</groupId>
      <artifactId>jettison</artifactId>
      <version>1.5.7</version>
      <optional>true</optional>
    </dependency>
    <dependency>
      <groupId>javax.xml.bind</groupId>
      <artifactId>jaxb-api</artifactId>
      <version>2.4.0</version>
      <optional>true</optional>
    </dependency>
    <dependency>
      <groupId>javax.activation</groupId>
      <artifactId>activation</artifactId>
      <version>1.2.0</version>
      <optional>true</optional>
    </dependency>
  </dependencies>
</project>
EOF

%check
export JAVA_HOME=%{_jvmdir}/java-openjdk
export PATH=$JAVA_HOME/bin:$PATH
mkdir -p check
cat > check/Smoke.java <<'END'
import com.thoughtworks.xstream.XStream;
import com.thoughtworks.xstream.io.xml.StaxDriver;
public class Smoke {
	static void round(XStream xs, String label) {
		xs.allowTypes(new Class[]{String.class});
		Object back = xs.fromXML(xs.toXML("gradle"));
		if (!"gradle".equals(back)) {
			throw new AssertionError(label);
		}
		System.out.println(label + " ok");
	}
	public static void main(String[] args) {
		round(new XStream(new StaxDriver()), "stax");
		round(new XStream(), "default");
	}
}
END
javac --release 8 -encoding UTF-8 -Xlint:-options -cp %{name}.jar -d check check/Smoke.java
out=$(java -cp check:%{name}.jar:%{_javadir}/xmlpull.jar:%{_javadir}/mxparser.jar Smoke)
printf '%s\n' "$out"
printf '%s\n' "$out" | grep -q 'stax ok'
printf '%s\n' "$out" | grep -q 'default ok'

%install
sysjar install --buildroot %{buildroot} \
	--artifact %{name}.pom:%{name}.jar \
	--file-name %{name} \
	--filelist .mfiles

%files -f .mfiles
%doc LICENSE.txt README.md
