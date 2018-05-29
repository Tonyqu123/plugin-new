<style lang="scss">
  .new-project-dialog {
    .dao-dialog-wrapper .dao-dialog-container {
      height: auto;
    }
    .manage-wrap {
      display: flex;
    }
    .manage-btn {
      margin-left: 10px;
    }

    .dao-setting-content .dao-select {
      width: 100%;
    }

    .container-step-two {
      padding: 15px 20px;
      margin-top: 20px;
      background-color: #f5f7fa;

      .container-checkbox {
        margin-right: 5px;
      }

      .dao-select {
        margin-bottom: 10px;
        background-color: #fff;
      }
    }

    .project-dialog-footer {
      display: flex;

      .project-dialog-btn-group {
        flex: 1;
      }

      .error-msg {
        align-self: center;
        color: #f1483f;
      }
    }
  }
</style>
<template>
  <div class="new-project-dialog">
    <dao-dialog
      :config="config"
      :visible.sync="isShow"
      @dao-dialog-open="handleOpen"
      @dao-dialog-close="handleClose"
    >
      <div v-show="!isDownJob">
        <!-- @dao-dialog-cancel="handleCancel" -->
        <!-- @dao-dialog-confirm="handleConfirm" -->
        <dao-setting-section>
          <div slot="label">
            <span>
              作业
            </span>
          </div>
          <div slot="content" class="manage-wrap">
            <dao-select
              v-if="jobs && jobs.length > 0"
              v-model="selectedJob"
              placeholder="选择一个作业"
              no-data-text="无选项">
              <dao-option v-for="job in jobs" :key="job" :value="job" :label="job.Name"></dao-option>
            </dao-select>
            <button
              class="dao-btn ghost manage-btn"
              @click="handleManageJobs()">
              配置作业
            </button>
          </div>
        </dao-setting-section>
        <dao-setting-section>
          <div slot="label">
            <span>
              选择容器
            </span>
          </div>
          <div slot="content">
            <dao-radio-group>
              <dao-radio label="all" v-model.lazy="selectedContainerOne">在某一个服务下的所有容器上执行</dao-radio>
              <dao-radio label="one" v-model.lazy="selectedContainerOne">在选择的容器上执行</dao-radio>
            </dao-radio-group>
            <div class="container-step-two">
              <dao-select
                v-model="selectedService"
                placeholder="选择一个服务"
                no-data-text="无选项">
                <dao-option
                  v-for="item in services"
                  :key="item.id"
                  :value="item"
                  :label="item.name" />
              </dao-select>
              <!-- 还有一个选项 -->
              <StyleTable
                :height="4"
                v-if="selectedContainerOne === 'one' && selectedService">
                <tr slot="head">
                  <th>
                    容器
                  </th>
                </tr>
                <tr
                  slot="body"
                  :key="container.ID"
                  v-for="(container, index) in containers[selectedService.name]">
                  <td v-if="container">
                    <input
                      class="container-checkbox"
                      type="checkbox"
                      v-model="container.isChecked"/>
                    {{selectedService.name}}.{{container.Slot}}
                  </td>
                </tr>
              </StyleTable>
            </div>
          </div>
        </dao-setting-section>
      </div>
      <!-- 执行的作业是回收作业时 -->
      <div v-show="isDownJob" style="height: 200px;">
        <dao-setting-section>
          执行作业后删除容器
          <dao-select v-model="deleteContainerAfterJob" size="sm" style="display: inline-block;width: 80px;">
            <dao-option :value="true" label="Yes"></dao-option>
            <dao-option :value="false" label="No"></dao-option>
          </dao-select>
        </dao-setting-section>
      </div>
      <div class="project-dialog-footer" slot="footer">
        <div
          v-if="isErrorShow"
          class="error-msg">
          请选择至少一个{{errorMsg}}。
        </div>
        <div class="project-dialog-btn-group">
          <button
            class="dao-btn ghost"
            :disabled="isAllreadyStart"
            @click="cancel()">取消</button>
          <button
            class="dao-btn blue"
            :disabled="isAllreadyStart"
            @click="startProxy()">确定</button>
        </div>
      </div>
    </dao-dialog>
  </div>
</template>

<script>
/**
 * 事件:
 * handleManageJobs: 点击配置作业
 * hasNewProject: 点击开始新任务 -> 传递参数
 *
 */
/* eslint-disable no-plusplus */
import Utils from '../../utils/index';
import ApiService from '../../common/apiService';
import StyleTable from '../styleTable/StyleTable';

export default {
  name: 'NewProjectDialog',
  props: {
    jobList: {
      type: Array,
      require: true,
    },
    appName: {
      type: String,
      require: true,
    },
    visible: {
      type: Boolean,
      require: true,
      default: false,
    },
  },
  data() {
    return {
      config: {
        type: 'normal',
        title: '执行作业',
        showHeader: true,
        showFooter: true,
        closeOnClickOutside: true,
        closeOnPressEscape: true,
      },
      isShow: this.visible,
      // error 是否信息显示
      isErrorShow: false,
      errorMsg: '容器',
      isSelectJobShow: true,
      cache: {
        services: null,
        jobs: null,
        containers: null,
      },
      services: [],
      containers: {},
      // containers: [],
      ContainersOne: [],
      selectedService: null,
      // 选择容器第一步:
      // 可选值 有 all , one,
      // all: 某一个服务下的所有容器
      // one: 在选择的容器上
      selectedContainerOne: 'all',
      selectedJob: null,
      isAllreadyStart: false,
      jobs: [],
      isDownJob: false,
      deleteContainerAfterJob: false,
    };
  },
  computed: {
    // jobs() {
    //   return this.jobList;
    // },
  },
  methods: {
    // handleOpen 请求数据,
    //  初始化
    handleOpen() {
      this.init();
      this.errorMsg = '容器';
    },
    // reset
    handleClose() {
      this.isAllreadyStart = false;
      this.initSelected();
      this.transformContainers();
    },
    transformContainers() {
      this.$emit('transformContainers', this.containers);
    },
    // 配置作业
    handleManageJobs() {
      this.$emit('handleManageJobs');
    },
    // close
    close() {
      this.isShow = false;
    },
    // 检测要开始的任务名称
    startProxy() {
      if (this.selectedJob.Name === 'down' && !this.isDownJob) {
        this.isDownJob = true;
      } else {
        this.start();
      }
    },
    // 开始新任务
    start() {
      if (!this.checkIsAll()) {
        this.isErrorShow = true;
        return;
      }

      this.isAllreadyStart = true;
      this.isErrorShow = false;
      const Target = [];
      // const transCons = {};
      // 获取选择的容器列表

      const runningContainers = this.filterContainers();
      runningContainers
        .forEach(({ NodeId, ContainerId }) => {
        // .forEach(({ NodeId, ContainerId, ...rest }) => {
          if (ContainerId) {
            Target.push({
              ContainerId,
              NodeId,
            });
            // transCons[ContainerId] = rest;
          }
        });

      this.startJobs(Target, runningContainers);
    },
    cancel() {
      if (this.isDownJob) {
        this.isDownJob = false;
        return;
      }
      this.isAllreadyStart = true;
      this.close();
    },
    startJobs(Target, transCons) {
      ApiService.startJobs(this.selectedJob.JobId, {
        Target,
        is_remove: this.deleteContainerAfterJob,
      }).then((res) => {
        const params = {
          job: res,
          containers: transCons,
        };
        Utils.createNoty('成功开始新任务!', 'success');
        this.$emit('hasNewProject', params);
        this.close();
      }, (error) => {
        Utils.createNoty(`${error.body.id === 'job_id_not_found' ? '作业 ID 未找到' : '新任务开始失败'}, 请重试!`, 'error');
        this.isAllreadyStart = false;
      });
    },
    // get services
    getServices(name = this.appName) {
      return ApiService.getServices(name)
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
      return ApiService.getTasks(serviceId)
        .then(data => data);
    },
    // check
    checkIsAll() {
      // console.log('check');
      if (!this.selectedJob) {
        this.errorMsg = '作业';
        return false;
      }
      if (this.selectedContainerOne === 'all' && this.selectedService) {
        const selectName = this.selectedService.name;
        const containerLen = this.detectLength(this.containers[selectName], 4);
        if (containerLen < 1) {
          return false;
        }
        return true;
      }
      if (this.selectedContainerOne === 'one') {
        return Object.keys(this.containers)
          .some(name => this.containers[name].some(item => item.isChecked));
      }
      return false;
    },
    // 过滤出 选中的 container
    filterContainers() {
      const tempContainers = [];
      if (this.selectedContainerOne === 'all') {
        this.containers[this.selectedService.name]
          .forEach((item) => {
            if (!item) return;
            const { Status, NodeID, Slot } = item;
            tempContainers.push({
              name: `${this.selectedService.name}.${Slot}`,
              service: this.selectedService.name,
              ContainerId: Status.ContainerStatus.ContainerID,
              NodeId: NodeID,
              Slot,
            });
          });
        return tempContainers;
      }

      Object.keys(this.containers)
        .forEach((name) => {
          this.containers[name]
            .forEach((item) => {
              const { Status, NodeID, isChecked, Slot } = item;
              if (!item || !isChecked) return;
              tempContainers.push({
                name: `${name}.${Slot}`,
                service: name,
                ContainerId: Status.ContainerStatus.ContainerID,
                NodeId: NodeID,
                Slot,
              });
            });
        });
      return tempContainers;
    },
    // 数据 init
    init() {
      this.getServices(this.appName)
        .then((services) => {
          this.cache.services = services;
          services.forEach((service) => {
            this.containers[service.name] = this.initContainers(4);
            this.getContainers(service.id)
              .then((list) => {
                this.containers[service.name] =
                this.addDatas(list, this.containers[service.name], 4);
                this.cache.containers = this.containers;
                this.initSelected();
              });
          });
        });
    },
    initContainers(height) {
      const temp = [];
      for (let i = 0; i < height; i++) {
        temp.push(0);
      }
      return temp;
    },
    initSelected() {
      if (this.jobs.length > 0) {
        this.selectedJob = this.jobs[0];
      }
      if (this.services.length > 0) {
        // 设置 选中的 作业
        this.selectedService = this.services[0];
      }

      this.selectedContainerOne = 'all';
    },
    // 向 styleTable 中增加 数据
    // @params datas (Array), 需要添加的 数据
    addDatas(datas, curDatas, height) {
      const len = this.detectLength(curDatas, height);
      let result = curDatas;

      if (len >= height) {
        result = [
          ...curDatas,
          ...datas,
        ];
      } else {
        datas.forEach((data, idx) => {
          result[len + idx] = data;
        });
      }
      return result;
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
      this.isDownJob = false;
    },
    isShow(newV) {
      if (newV === this.visible) return;
      this.$emit('update:visible', newV);
    },
    jobList(newV) {
      if (!newV) {
        this.jobs = [];
      } else {
        this.jobs = newV;
        if (!this.selectedJob || !newV) return;
        this.selectedJob = null;
      }
    },
  },
  components: {
    StyleTable,
  },
};
</script>

