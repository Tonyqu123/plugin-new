<style lang="scss" scoped>
  .dao-table-container {
    padding-top: 0;
  }
  .dao-table-toolbar {
    height: auto;
    margin-bottom: 10px;
  }

  .table-filters .refresh-btn {
    height: 32px;
    padding: 8px 7px;
  }
  .search-btn {
    padding: 8px 7px;
    margin-left: 10px;
  }
  .page-btn-group {
    margin-top: 20px;

    .btn-group .dao-btn {
      margin: 0;

      &:first-child {
        border-radius: 4px 0 0 4px;
        border-right-style: none;
      }

      &:last-child {
        border-radius: 0 4px 4px 0;
      }
    }

    &>P {
      display: inline-block;
      margin-left: 20px;
    }
  }
</style>
<template>
  <div class="wrap">
    <NewProjectDialog
      :visible.sync="isAddNewProject"
      :jobList="jobs"
      :appName="appName"
      @handleManageJobs="manageProjects"
      @transformContainers="getAppContainers"
      @hasNewProject="hasNewProject"/>
    <EditJobDialog
      :visible.sync="isEditJobShow"
      :appName="appName"
      :jobList.sync="jobs"
      @closeEditJob="handleEditClose"/>
    <LogDialog
      :visible.sync="isLogShow"
      :logUrl="logUrl"
      :logs="selectLogs" />
    <div class="dao-table-container">
      <div class="dao-table-toolbar">
        <div class="btn-group">
          <button
            @click="startNewProjects()"
            class="dao-btn blue">
            执行作业
          </button>
        </div>
        <div class="table-filters">
          <input
            class="dao-control search search-input"
            ref="searchInput"
            type="text"
            placeholder="搜索"
            @keyup="debounceSearch"
            v-model.trim="searchWord" />
          <div
            @click="refresh()"
            :disabled="!this.curJob"
            class="dao-btn ghost refresh-btn">
            <svg>
              <use xlink:href="#icon_update"></use>
            </svg>
          </div>
        </div>
      </div>
      <container-list
        :curJob="curJob"
        @selectCon="showLog"
        :containers="curContainers" />
        <!-- :containers="containersList" /> -->
      <div class="dao-table-toolbar page-btn-group">
        <div class="btn-group clearfix">
          <button
            class="dao-btn ghost has-icon"
            :disabled="curPage < 1"
            @click.prevent="pre()">
            <svg class="icon"><use xlink:href="#icon_caret-left"></use></svg>
          </button><!--
          --><button
            class="dao-btn ghost has-icon"
            :disabled="checkIsDisableNext(historyJobList)"
            @click.prevent="next()">
              <svg class="icon"><use xlink:href="#icon_caret-right"></use></svg>
            </button>
        </div><!--
        --><p>
          第 {{curPage + 1}} 页， {{start + 1}} - {{end}}
        </p>
      </div>
    </div>
  </div>
</template>
<script>
  import Utils from '../../utils/index';
  import ContainerList from '../../components/containerList/ContainerList';
  import NewProjectDialog from '../../components/newProjectDialog/NewProjectDialog';
  import EditJobDialog from '../../components/editJobDialog/EditJobDialog';
  import LogDialog from '../../components/logDialog/LogDialog';
  import ApiService from '../../common/apiService';
  import MixService from '../../common/mixService';

  export default {
    data() {
      return {
        // appName: '2048',
        appName: this.getAppName() || '2048',
        // 当前正在进行的作业
        curJob: null,
        // 同步 jobs 给 editJobs 和 NewProject
        jobs: null,
        // containers 数据, object， 带有 containersList 顺序
        // containers: null,
        serviceContainers: null,
        // dialog
        isAddNewProject: false,
        isEditJobShow: false,
        // log
        isLogShow: false,
        selectLogs: null,
        logUrl: null,
        curPage: 0,
        limit: 10,
        // cache
        cache: {},
        historyJobList: [],
        searchWord: null,
        runningContainers: [],
      };
    },
    computed: {
      start() {
        if (!this.historyJobList || this.historyJobList.length < 1) {
          return -1;
        }
        return this.curPage * this.limit;
      },
      end() {
        if (!this.historyJobList || this.historyJobList.length < 1) {
          return 0;
        }
        const cons = this.historyJobList;
        return cons[(this.curPage + 1) * this.limit] ?
          ((this.curPage + 1) * this.limit) : cons.length;
      },
      // 当前显示
      curContainers() {
        const cons = !this.historyJobList ? [] : this.historyJobList.slice();
        if (!cons || cons.length === 0) return [];
        cons.reverse();
        return cons.slice(this.start, this.end);
      },
      jobListFrom() {
        return this.transformJobForm(this.jobs);
      },
    },
    methods: {
      startNewProjects() {
        this.searchWord = null;
        this.historyJobList = this.cache.history;
        if (this.curJob && this.curJob.JobId) {
          this.handleClearJobs();
          this.isAddNewProject = true;
        } else {
          this.isAddNewProject = true;
        }
      },
      manageProjects() {
        this.isEditJobShow = true;
      },
      refresh() {
        if (!this.curJob || !this.curJob.JobId) return;
        this.historyJobList = this.cache.history;
        this.searchWord = null;
        /* eslint-disable consistent-return */
        return this.getJobHistory()
          .then((res) => {
            this.historyJobList = this.transformHistoryContainers(res);
            this.cache.history = this.historyJobList;
          }, () => {
            Utils.createNoty('刷新失败, 请重试!', 'error');
          });
      },
      showLog(index) {
        if (this.curContainers[index]) {
          const { ContainerId, JobId } = this.curContainers[index];
          const Executor = this.jobListFrom[JobId].Executors;
          // console.log('Executor', Executor);
          this.logUrl = `./api/jobs/${JobId}/log/${Executor}?ContainerId=${ContainerId}`;
          this.selectLogs = this.curContainers[index].Output;
          this.isLogShow = true;
        }
      },
      pre() {
        if (this.curPage < 1) return;
        this.curPage -= 1;
      },
      next() {
        const len = this.historyJobList.length;
        if (this.curPage * this.limit >= len) return;
        this.curPage += 1;
      },
      // 搜索历史记录
      search(e) {
        this.curPage = 0;
        if (e.keyCode === 13) {
          this.$refs.searchInput.blur();
        }
        this.historyJobList = this.filterSearch(this.searchWord);
      },
      debounceSearch() {},
      // 过滤搜索的 word
      filterSearch(keyWord) {
        if (!keyWord || keyWord === '') {
          return this.cache.history;
        }

        return this.cache.history
          .filter((item) => {
            const { name, service, Status, JobName, JobId, StatusMsg, displayTime } = item;
            if (name.indexOf(keyWord) !== -1 ||
              service.indexOf(keyWord) !== -1 ||
              Status.indexOf(keyWord) !== -1 ||
              JobName.indexOf(keyWord) !== -1 ||
              JobId.indexOf(keyWord) !== -1 ||
              displayTime.indexOf(keyWord) !== -1 ||
              StatusMsg.indexOf(keyWord) !== -1) {
              return true;
            }

            return false;
          });
      },
      hasNewProject({ job, containers: datas }) {
        this.curJob = job;
        this.runningContainers = datas;
        this.jobs = this.jobs
          .map((item) => {
            if (item.JobId !== job.JobId) {
              return item;
            }
            return {
              ...item,
              Executors: job.Executors,
            };
          });
        this.cache.jobs = this.jobs;
        this.getJobHistory()
          .then((res) => {
            this.historyJobList = this.transformHistoryContainers(res);
            this.cache.history = this.historyJobList;
          });
      },
      // 从开始新任务 -> 管理作业，
      // 当管理作业页面关闭时，开始新任务需要更新
      handleEditClose(data) {
        this.jobs = data;
      },
      handleClearJobs() {
        this.curJob = null;
        // this.containers = null;
      },
      // 从 执行 作业返回的
      getAppContainers(data) {
        this.serviceContainers = data;
      },
      // get 作业
      getJobs() {
        return ApiService.getJobs(this.appName)
          .then((data) => {
            this.cache.jobs = data;
            this.jobs = data;
            return data;
          });
      },
      // get App Name (service name)
      getAppName() {
        const queryList = window.location.search.substr(1).split('&');
        const nameQuery = queryList.filter(query => query.startsWith('ObjectId'));
        if (nameQuery[0]) {
          return nameQuery[0].split('=')[1];
        }
        return false;
      },
      //  History 部分
      getServiceContainers(name = this.appName) {
        return MixService.getServiceContainers(name)
          .then((data) => {
            this.cache.serviceContainers = data;
            this.serviceContainers = data;
            return data;
          });
      },
      getJobHistory(name = this.appName) {
        return ApiService
          .getJobHistory(name)
          .then((data) => {
            // this.cache.history = data;
            this.history = data;
            return data;
          });
      },
      // 将 job 转换成{ id: name }格式
      transformJobForm(jobs = this.jobs) {
        if (!jobs) return null;
        return jobs
          .reduce((pre, cur) => {
            const len = cur.Executors.length;
            return {
              ...pre,
              [cur.JobId]: {
                name: cur.Name,
                Executors: len === 0 ? '' : cur.Executors[len - 1],
              },
            };
          }, {});
      },
      // 输入 history 返回的 containers
      // 返回 可以显示到 containerList 组件的 列表
      transformHistoryContainers(resCons) {
        const temp = [];
        resCons.forEach((con) => {
          let flag = false;
          let JobName = '';
          let getTask = null;
          // 根据 JobId 找相应的 JobName
          if (!this.jobListFrom) {
            this.jobs
              .forEach((job) => {
                if (job.JobId === con.JobId) {
                  JobName = job.JobName;
                }
              });
          } else {
            JobName = this.jobListFrom[con.JobId].name || '';
          }
          // 根据 containerId 找相应的 name, serviceName
          Object.keys(this.serviceContainers || {})
            .forEach((key) => {
              if (Object.prototype.hasOwnProperty.call(this.serviceContainers, key)) {
                // 相应的 name 为 key 的相关 Containers
                const serviceTasks = this.serviceContainers[key];
                const getTaskList = serviceTasks
                  .filter((task) => {
                    if (!task) return false;
                    if (task.Status.ContainerStatus.ContainerID === con.ContainerId) return true;
                    return false;
                  });

                // console.log('getTaskList', getTaskList)
                if (getTaskList.length < 1) {
                  flag = false;
                } else {
                  flag = true;
                  getTask = getTaskList[0];
                }

                // console.log('taskList', getTaskList);

                if (flag) {
                  const nowLen = temp.length;
                  temp[nowLen] = {
                    ...con,
                    JobName,
                    StatusMsg: this.getStatus(con),
                    displayTime: Utils.timeConverter(con.StartTime),
                    service: key,
                    name: `${key}.${getTask.Slot}`,
                  };
                }
              }
            });
        });
        return temp;
      },
      getHistoryJobList() {
        const promiseList = [];
        // 得到 job, 在 this.jobs 中
        promiseList.push(this.getJobs());
        // 得到 services 和对应的 containers, 在 this.serviceContainers 中
        promiseList.push(this.getServiceContainers());
        // 得到 history
        promiseList.push(this.getJobHistory());

        Promise.all(promiseList)
          .then((dataList) => {
            this.historyJobList = this.transformHistoryContainers(dataList[2]);
            this.cache.history = this.historyJobList;
          });
      },
      checkIsDisableNext(datas) {
        if (!datas) return true;
        return datas.length <= (this.curPage + 1) * this.limit;
      },
      getStatus(container) {
        let statusMsg = '失败';
        const { Status, ExitCode } = container;
        if (Status === 'STARTING' || Status === 'CREATED') {
          statusMsg = '等待中';
        } else if (Status === 'FINISHED') {
          if (ExitCode === 0) {
            statusMsg = '成功';
          }
        }
        return statusMsg;
      },
    },
    watch: {
      jobs: {
        handler() {
          this.getJobHistory()
            .then((res) => {
              this.historyJobList = this.transformHistoryContainers(res);
              this.cache.history = this.historyJobList;
            });
        },
        deep: true,
      },
    },
    created() {
      this.getHistoryJobList();
      this.debounceSearch = this.$lodash.debounce(this.search, 500);
    },
    components: {
      ContainerList,
      NewProjectDialog,
      EditJobDialog,
      LogDialog,
    },
  };
</script>
