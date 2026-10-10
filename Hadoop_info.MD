# hadoop端口信息

> 端口格式：**默认端口(修改xxx)** = 官方默认值，括号内为本集群实际配置；无括号表示未修改。
> 端口开放列遵循约定：**箭头方向 = 主动连接发起方**，防火墙在"被连方"放行对应端口。

## 进程说明

| 进程 | 所属体系 | 定位 |
| --- | --- | --- |
| NameNode | HDFS | 控制面：管理文件元数据、块映射、DataNode 调度 |
| DataNode | HDFS | 数据面：存储实际数据块，执行读写/复制 |
| SecondaryNameNode | HDFS | 辅助面：合并 NameNode edits 日志为 fsimage（检查点，非热备） |
| JournalNode | HDFS (HA) | 高可用：Active/Standby NameNode 间同步 edits 日志 |
| ZKFC | HDFS (HA) | 高可用：监控 NameNode 健康，借助 ZK 自动故障转移 |
| ResourceManager | YARN | 控制面：集群资源分配、作业调度 |
| NodeManager | YARN | 数据面：单节点资源代理，启动/监控 Container |
| ApplicationMaster | YARN | 应用级：每个作业一个，向 RM 申请资源并协调任务 |
| JobHistoryServer | YARN / MapReduce | 辅助面：已完成作业的历史信息存档与查询 |
| TimelineServer | YARN | 辅助面：作业/任务通用时间线指标收集 |
| ZooKeeper | 分布式协调 | 基础设施：选主、分布式锁、配置同步（HDFS/RM HA、HBase、Kafka、Kyuubi 均依赖） |
| Hive MetaStore | Hive | 元数据中心：表结构、分区等元数据的存储与查询服务 |
| HiveServer2 | Hive | SQL网关：JDBC/ODBC 入口，将 HQL 转为计算任务（本集群由 Kyuubi 替代） |
| Kyuubi | Spark 生态 | SQL网关：多租户 JDBC 统一入口，后端调度 Spark 引擎 |
| Spark Master | Spark | 控制面：Standalone 模式的集群资源管理（本集群走 YARN，未部署） |
| Spark Worker | Spark | 数据面：Standalone 模式的执行节点（本集群由 NodeManager 承担） |
| Spark HistoryServer | Spark | 辅助面：Spark 应用历史日志查看 |
| HBase Master | HBase | 控制面：Region 分配、负载均衡（未部署） |
| HBase RegionServer | HBase | 数据面：Region 读写服务（未部署） |
| Kafka Broker | Kafka | 消息队列：高吞吐日志/流数据管道（未部署） |
| Flink JobManager | Flink | 控制面：流作业调度与 checkpoint 协调（未部署） |
| Flink TaskManager | Flink | 数据面：流任务实际执行节点（未部署） |

## 端口信息

| 进程 | 端口 | 说明 |
| --- | --- | --- |
| NameNode | 8020(修改9000) | RPC：客户端读写请求、DN心跳/块汇报、SNN拉取edits |
| NameNode | 9870(修改50070) | HTTP：HDFS 控制面板（Web UI） |
| DataNode | 9866 | 数据传输：客户端读写 block、DN→DN 管道复制（数据面，流量最大） |
| DataNode | 9867 | IPC：NameNode 下发指令（复制块/删除块） |
| DataNode | 9864 | HTTP：DN 状态页 |
| SecondaryNameNode | 9868(修改50090) | HTTP：SNN 状态页；NN 从这里下载合并后的 fsimage |
| JournalNode | 8485 | RPC：双 NameNode 之间同步 edits 日志 |
| JournalNode | 8480 | HTTP：JN 状态页 |
| ZKFC | 8019 | HTTP：NN 故障转移控制器状态页 |
| ResourceManager | 8032 | 客户端 RPC：提交作业、查询应用状态 |
| ResourceManager | 8030 | Scheduler：ApplicationMaster 申请资源 |
| ResourceManager | 8031 | ResourceTracker：所有 NodeManager 心跳（每秒） |
| ResourceManager | 8033 | Admin：节点退役/刷新等管理命令 |
| ResourceManager | 8088 | HTTP：YARN 作业监控页面 |
| NodeManager | 8041 | ContainerManager：AM 命令 NM 启动/停止容器 |
| NodeManager | 8040 | 资源本地化：下载任务依赖（jar/文件）到容器目录 |
| NodeManager | 8042 | HTTP：NM 节点状态页 |
| NodeManager | 13562 | Shuffle：Reduce 任务跨节点拉取 Map 中间数据 |
| JobHistoryServer | 10020 | RPC：历史作业信息查询 |
| JobHistoryServer | 19888 | HTTP：MR 历史作业页面 |
| TimelineServer | 10200 | RPC：时间线数据写入/查询 |
| TimelineServer | 8188 | HTTP：时间线页面 |
| ZooKeeper | 2181 | 客户端端口：选主、锁、HA 协调（所有依赖组件连接） |
| ZooKeeper | 2888 | ZK 集群内部：Follower→Leader 数据同步 |
| ZooKeeper | 3888 | ZK 集群内部：Leader 选举 |
| Hive MetaStore | 9083(修改10019) | Thrift：Spark/Kyuubi 查询表结构、分区等元数据 |
| HiveServer2 | 10000 | Thrift：JDBC/ODBC SQL 入口（本集群由 Kyuubi 替代，未部署） |
| HiveServer2 | 10002 | HTTP：HiveServer2 Web UI |
| Kyuubi | 10009(修改10019) | JDBC：业务应用 SQL 统一入口，后端拉起 Spark 引擎 |
| Spark Master | 7077 | RPC：Standalone 模式客户端提交入口（未部署） |
| Spark Master | 8080(冲突时改6066) | HTTP：Master 状态页（与 RM/YARN 8088 区分） |
| Spark Worker | 7078 | RPC：Worker 与 Master 通信 |
| Spark Worker | 8081 | HTTP：Worker 状态页 |
| Spark HistoryServer | 18080 | HTTP：Spark 应用历史页面 |
| HBase Master | 16000 | RPC：HBase 主节点通信 |
| HBase Master | 16010 | HTTP：HBase Master 页面 |
| HBase RegionServer | 16020 | RPC：Region 读写服务 |
| HBase RegionServer | 16030 | HTTP：RegionServer 页面 |
| Kafka Broker | 9092 | 客户端/生产消费通信端口 |
| Kafka Broker | 9093 | 集群内部 Broker 间复制通信 |
| Flink JobManager | 6123 | RPC：Flink 作业提交与协调 |
| Flink JobManager | 8081 | HTTP：Flink Web 控制台（与 Spark Worker 撞号，部署时注意） |
| Flink TaskManager | 6122 | RPC：TaskManager 通信（数据交换走其数据端口） |

## 端口访问

| 进程 | 端口 | 端口开放 | 原因 |
| --- | --- | --- | --- |
| NameNode | 8020 | 所有DN、SNN节点 + 客户端网段 | DN心跳注册、块汇报，SNN拉取，客户端读写 |
| NameNode | 9870 | 按需开放（运维网段） | HDFS 控制面板 |
| DataNode | 9866 | 所有节点互通 | DN数据读写/管道复制，客户端直连读block |
| DataNode | 9867 | 仅 NameNode 节点 | NN 主动连 DN 下发复制/删除指令 |
| DataNode | 9864 | 按需开放（运维网段） | DN 状态页 |
| SecondaryNameNode | 9868 | 仅 NameNode 节点 | NN 下载合并后的新 fsimage |
| JournalNode | 8485 | 双 NN 节点 + 其他 JN 节点 | edits 日志同步写入 |
| JournalNode | 8480 | 按需开放（运维网段） | JN 状态页 |
| ZKFC | 8019 | 按需开放（运维网段） | 故障转移状态查看 |
| ResourceManager | 8031 | 所有 NM 节点 | NodeManager 心跳注册 |
| ResourceManager | 8030 | 集群内（AM 所在节点） | ApplicationMaster 申请资源 |
| ResourceManager | 8032 | 客户端网段 + 集群内 | 提交作业、查询应用状态 |
| ResourceManager | 8033 | 仅本机/运维网段 | 管理命令（节点退役等） |
| ResourceManager | 8088 | 按需开放（运维/业务查看） | YARN 作业监控页面 |
| NodeManager | 8041 | 集群内（AM 所在节点） | AM 命令启动/停止容器 |
| NodeManager | 8040 | 集群内 | 任务依赖本地化下载 |
| NodeManager | 13562 | 所有 NM 节点互通 | Shuffle 中间数据拉取（Map→Reduce） |
| NodeManager | 8042 | 按需开放（运维网段） | NM 节点状态页 |
| JobHistoryServer | 10020 | 仅 RM 节点 | 作业完成后 AM 归档历史信息 |
| JobHistoryServer | 19888 | 按需开放（运维网段） | 历史作业查看 |
| TimelineServer | 10200 | 集群内 | 指标收集写入/查询 |
| TimelineServer | 8188 | 按需开放（运维网段） | 时间线页面 |
| ZooKeeper | 2181 | 集群内所有 Hadoop 节点 | HA 选主、协调（ZKFC/RM/Kyuubi/HBase/Kafka 连接） |
| ZooKeeper | 2888/3888 | ZK 节点之间 | 集群内部同步与选举 |
| Hive MetaStore | 9083 | 所有跑 Spark 的节点 | Spark 引擎查询表/分区元数据 |
| HiveServer2 | 10000 | 客户端网段（如部署） | JDBC/ODBC SQL 入口 |
| Kyuubi | 10009 | 业务应用服务器 | JDBC 入口，提交 SQL |
| Spark Master | 7077 | 客户端网段（如部署） | Standalone 模式作业提交 |
| Spark Master/Worker | 8080/8081 | 按需开放（运维网段） | Spark 状态页 |
| Spark HistoryServer | 18080 | 按需开放（运维网段） | Spark 应用历史查看 |
| HBase Master | 16000/16010 | 集群内 + 运维网段 | HBase 主节点通信与页面 |
| HBase RegionServer | 16020 | Master + 其他 RegionServer | Region 数据读写与复制 |
| HBase RegionServer | 16030 | 按需开放（运维网段） | RegionServer 页面 |
| Kafka Broker | 9092 | 生产/消费客户端网段 | 消息收发 |
| Kafka Broker | 9093 | Kafka 节点之间 | Broker 间副本同步 |
| Flink JobManager | 6123/8081 | 客户端网段 + 运维网段 | 作业提交与 Web 控制台 |
| Flink TaskManager | 6122 | JobManager + 其他 TaskManager | 任务执行与数据交换 |

## 备注

1. 防火墙默认策略 INPUT DROP + conntrack 状态下，回程流量自动放行，只需配置上表"新建连接"方向。
2. 各守护进程还会有 1~3 个 127.0.0.1:<随机端口>，是 JVM 内部服务（JMX 等），重启即变，回环地址外部不可达，无需列入防火墙规则。
3. 本集群端口为自定义配置（如 8020→9000、10009→10019、9083→10019），排查问题时以实际配置为准：`hdfs getconf -confKey <参数名>`。
4. 进程表中标注"未部署"的组件为生态常用扩展，规划扩容时可按对应端口预留防火墙策略。
