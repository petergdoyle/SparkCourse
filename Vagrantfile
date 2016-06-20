
Vagrant.configure(2) do |config|

  config.vm.box = "petergdoyle/CentOS-7-x86_64-Minimal-1503-01"

  config.vm.provider "virtualbox" do |vb|
    vb.customize ["modifyvm", :id, "--cpuexecutioncap", "80"]
    vb.cpus=2
    vb.memory = "2048"
  end

  config.vm.provision "shell", inline: <<-SHELL

  #best to update the os
  yum -y update && yum -y clean
  yum -y install vim htop curl wget tree unzip bash-completion


  eval "yum repolist |grep 'epel/x86_64'" > /dev/null 2>&1
  if [ $? -eq 1 ]; then
    yum -y install epel-release
  else
    echo -e "\e[7;44;96m*epel-release already appears to be installed. skipping."
  fi

  eval 'python' > /dev/null 2>&1
  if [ $? -eq 127 ]; then
    yum install -y python34
  else
    echo -e "\e[7;44;96m*python34 already appears to be installed. skipping."
  fi

  eval 'pip -help' > /dev/null 2>&1
  if [ $? -eq 127 ]; then
     yum -y install python-pip
  else
   echo -e "\e[7;44;96m*python-pip already appears to be installed. skipping."
  fi

  eval 'java -version' > /dev/null 2>&1
  if [ $? -eq 127 ]; then
    mkdir -p /usr/java
    #install java jdk 8 from oracle
    curl -O -L --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie" \
    "http://download.oracle.com/otn-pub/java/jdk/8u60-b27/jdk-8u60-linux-x64.tar.gz" \
      && tar -xvf jdk-8u60-linux-x64.tar.gz -C /usr/java \
      && ln -s /usr/java/jdk1.8.0_60/ /usr/java/default \
      && rm -f jdk-8u60-linux-x64.tar.gz

    alternatives --install "/usr/bin/java" "java" "/usr/java/default/bin/java" 99999; \
    alternatives --install "/usr/bin/javac" "javac" "/usr/java/default/bin/javac" 99999; \
    alternatives --install "/usr/bin/javaws" "javaws" "/usr/java/default/bin/javaws" 99999; \
    alternatives --install "/usr/bin/jvisualvm" "jvisualvm" "/usr/java/default/bin/jvisualvm" 99999

    export JAVA_HOME=/usr/java/default
    cat >/etc/profile.d/java.sh <<-EOF
export JAVA_HOME=$JAVA_HOME
EOF

  else
    echo -e "\e[7;44;96m*jdk-8u60-linux-x64 already appears to be installed. skipping."
  fi


  if [ ! -d /usr/spark/spark-1.6.1-bin-hadoop2.6/ ]; then
    mkdir -p /usr/spark
    curl -O -L http://www-eu.apache.org/dist/spark/spark-1.6.1/spark-1.6.1-bin-hadoop2.6.tgz \
      && tar -xvf spark-1.6.1-bin-hadoop2.6.tgz -C /usr/spark \
      && ln -s /usr/spark/spark-1.6.1-bin-hadoop2.6/ /usr/spark/default \
      && rm -f spark-1.6.1-bin-hadoop2.6.tgz

    export SPARK_HOME=/usr/spark/default
    cat >/etc/profile.d/spark.sh <<-EOF
export SPARK_HOME=$SPARK_HOME
EOF

    #set log levels
    cp /usr/spark/default/conf/log4j.properties.template /usr/spark/default/conf/log4j.properties
    sed -i 's/INFO/ERROR/g' /usr/spark/default/conf/log4j.properties

    #install executeable files
    for each in $(find /usr/spark/default/bin/ -executable -type f) ; do
      name=$(basename $each)
      alternatives --install "/usr/bin/$name" "$name" "$each" 99999
    done


  else
    echo -e "\e[7;44;96m*spark-1.6.1 already appears to be installed. skipping."
  fi

  #course material
  if [ ! -d ml-100k ]; then
    curl -O http://files.grouplens.org/datasets/movielens/ml-100k.zip \
    && unzip ml-100k.zip \
    && rm -f ml-100k.zip
  fi

  if [ ! -f ratings-counter.py ]; then
    curl -O https://raw.githubusercontent.com/minimav/udemy_spark/master/ratings-counter.py
  fi



  #set hostname
  hostnamectl set-hostname SparkCourse.vbx

  SHELL
end
