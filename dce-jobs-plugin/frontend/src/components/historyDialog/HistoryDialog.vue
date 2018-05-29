<style lang="scss" scoped>

  input.dao-control.search-input + .dao-btn.search-btn {
    margin: 0 15px 0 10px;
    padding: 5px 10px;
  }
  .header {
    align-self: center;
  }
</style>
<template>
  <div class="history-dialog">
    <dao-dialog
      :config="config"
      :visible.sync="isShow"
      @dao-dialog-open="handleOpen"
      @dao-dialog-close="handleClose"
    >
      <div class="dao-dialog-header header">
        <span> 历史记录 </span>

        <div class="dao-close">
          <input
            class="dao-control search search-input"
            size="sm"
            type="text"
            placeholder="搜索"
            v-model.trim="searchWord" />
          <button
            class="dao-btn ghost search-btn"
            @click="search">
          搜索
          </button>
          <div @click="close">
            <svg preserveAspectRatio="xMidYMid" width="34" height="34" viewBox="0 0 34 34">
              <path d="M17.000,0.001 C7.612,0.001 0.001,7.612 0.001,17.000 C0.001,26.388 7.612,33.999 17.000,33.999 C26.388,33.999 33.999,26.388 33.999,17.000 C33.999,7.612 26.388,0.001 17.000,0.001 ZM24.166,21.666 C24.166,21.666 21.666,24.166 21.666,24.166 C21.666,24.166 17.000,19.500 17.000,19.500 C17.000,19.500 12.334,24.166 12.334,24.166 C12.334,24.166 9.834,21.666 9.834,21.666 C9.834,21.666 14.500,17.000 14.500,17.000 C14.500,17.000 9.834,12.335 9.834,12.335 C9.834,12.335 12.334,9.834 12.334,9.834 C12.334,9.834 17.000,14.500 17.000,14.500 C17.000,14.500 21.666,9.834 21.666,9.834 C21.666,9.834 24.166,12.335 24.166,12.335 C24.166,12.335 19.500,17.000 19.500,17.000 C19.500,17.000 24.166,21.666 24.166,21.666 Z" id="path-1" fill-rule="evenodd"/>
            </svg>
          </div>
        </div>
      </div>
      <Loading
        v-if="isloading"
      />
      <ContainerList
        v-if="!isloading"
        :curJob="{}"
        type="history"
        @selectCon="showLog"
        :containers="containersList" />
    </dao-dialog>
  </div>
</template>
<script>
/**
 * 事件:
 *
 */
/* eslint-disable no-plusplus */
import ApiService from '../../common/apiService';
import ContainerList from '../../components/containerList/ContainerList';
import Loading from '../loading';

export default {
  name: 'HistoryDialog',
  props: {
    visible: {
      type: Boolean,
      require: true,
      default: false,
    },
    appName: {
      type: String,
      require: true,
    },
    jobList: {
      type: Array,
      require: true,
    },
  },
  data() {
    return {
      config: {
        type: 'normal',
        title: '历史记录',
        showHeader: false,
        showFooter: false,
        closeOnClickOutside: true,
        closeOnPressEscape: true,
        size: 'resize',
      },
      cache: {},
      isShow: this.visible,
      containers: {},
      containersList: [],
      cacheContainers: null,
      isloading: false,
      searchWord: null,
    };
  },
  computed: {
    jobListFrom() {
      if (!this.jobList) return null;
      return this.jobList
        .reduce((pre, cur) => ({
          ...pre,
          [cur.JobId]: cur.Name,
        }), {});
    },
  },
  methods: {
    // handleOpen 请求数据,
    //  初始化
    handleOpen() {
      this.init();
    },
    // reset
    handleClose() {
      this.searchWord = null;
      this.isloading = false;
    },
    close() {
      this.isShow = false;
    },
    search() {
      this.containersList = this.filterSearch(this.searchWord);
    },
    filterSearch(keyWord) {
      if (!keyWord || keyWord === '') {
        return this.cacheContainers;
      }

      return this.cacheContainers
        .filter((item) => {
          const { name, service, Status, JobName, JobId } = item;
          if (name.indexOf(keyWord) !== -1 ||
            service.indexOf(keyWord) !== -1 ||
            Status.indexOf(keyWord) !== -1 ||
            JobName.indexOf(keyWord) !== -1 ||
            JobId.indexOf(keyWord) !== -1) {
            return true;
          }

          return false;
        });
    },
    getJobHistory() {
      return ApiService
        .getJobHistory(this.appName);
    },
    showLog(index) {
      if (this.containersList[index]) {
        this.$emit('showLog', this.containersList[index].Output);
      }
    },
    transformHistoryContainers(resCons) {
      const temp = resCons;
      resCons.forEach((con, index) => {
        let JobName = '';
        if (!this.jobListFrom) {
          this.jobList
            .forEach((job) => {
              if (job.JobId === con.JobId) {
                JobName = job.JobName;
              }
            });
        } else {
          JobName = this.jobListFrom[con.JobId] || '';
        }

        Object.keys(this.containers)
          .forEach((service) => {
            if (Object.prototype.hasOwnProperty.call(this.containers, service)) {
              const serviceTask = this.containers[service];
              serviceTask
                .forEach((task) => {
                  if (!task) return;
                  if (task.Status.ContainerStatus.ContainerID === con.ContainerId) {
                    temp[index].service = service;
                    temp[index].name = `${service}.${task.Slot}`;
                    temp[index].JobName = JobName;
                  }
                });
            }
          });
        temp[index].JobName = JobName;
      });
      return temp;
    },

    // get services
    getServices(name = this.appName) {
      return ApiService.getServices(name, this.token)
        .then((data) => {
          this.services = data.Services.map(({ ID, Spec }) => ({
            id: ID,
            name: Spec.Name,
          }));
          return this.services;
        }, (error) => {
          throw Error(error);
        });
    },
    // get tasks (容器列表)
    getContainers(serviceId) {
      return ApiService.getTasks(serviceId, this.token)
        .then(data => data);
    },
    // 数据 init
    init() {
      this.isloading = true;
      /* eslint-disable */
      const promiseList = [];
      const promsieServices = this.getServices(this.appName)
        .then((services) => {
          this.cache.services = services;
          const promiseDatas = [];

          services.forEach((service) => {
            this.containers[service.name] = [];
            const tempProm = this.getContainers(service.id, this.token)
              .then((data) => ({ serviceName: service.name, data}));
            promiseDatas.push(tempProm);
          });

          return Promise.all(promiseDatas)
            .then(response => {
              response.forEach((tasks) => {
                this.containers[tasks.serviceName] = tasks.data;
                this.cache.containers = this.containers;
              });
              return this.containers;
            });
        });
      const promiseJobs = this.getJobHistory();

      promiseList.push(promsieServices, promiseJobs);

      Promise.all(promiseList)
        .then((res) => {
          this.containersList = this.transformHistoryContainers(res[1]);
          this.cacheContainers = [
            ...this.containersList,
          ];
          this.isloading = false;
        }, () => {
          this.isloading = false;
        });
    },
    // 实际长度
    detectLength(list, height) {
      const idx = list.indexOf(0);
      if (idx >= 0 && idx <= height - 1) {
        return idx;
      }
      return list.length;
    },
  },
  watch: {
    visible(newV, oldV) {
      if (newV === oldV || newV === this.isShow) return;
      this.isShow = newV;
    },
    isShow(newV) {
      if (newV === this.visible) return;
      this.$emit('update:visible', newV);
    },
  },
  components: {
    ContainerList,
    Loading,
  },
};
</script>

