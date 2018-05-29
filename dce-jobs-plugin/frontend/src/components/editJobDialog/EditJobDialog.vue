<style lang="scss">
  .edit-job-dialog {
    .eidt-dialog-main .dao-dialog-wrapper .dao-dialog-container {
      width: 70%;
      height: auto;
      min-width: 750px;
    }

    .deleteDialog .dao-dialog-wrapper .dao-dialog-container{
      height: auto;
    }

    .edit-content-wrap {
      margin: 21px 20px;
      display: flex;
    }

    .show-panel {
      width: 25%;

      .dao-table {
        border-radius: 0;
      }
    }

    .jobs-btn-group {
      border: solid 1px #e4e7ed;
      border-top: none;
    }

    .jobs-btn-group {
      &>span,
      &>label {
        display: inline-block;
        height: 26px;

        font-size: 14px;
        text-align: center;
        line-height: 26px;
        vertical-align: middle;
        border-right: solid 1px #e4e7ed;
        &.icon-btn {
          width: 26px;
        }

        &.word-btn {
          padding: 0 10px;
        }
      }

      .word-btn {
        position: relative;
        overflow: hidden;

        &>input[type="file"] {
          position: absolute;
          height: 100%;
          display: none;
        }
      }

    }

    .edit-panel {
      flex: 1;
      position: relative;
      padding: 10px 20px;
      background-color: #f5f7fa;
      border: solid 1px #e4e7ed;
      border-left: none;

      .title {
        line-height: 1;
        margin-bottom: 10px;

        &:not(:first-child) {
          margin-top: 20px;
        }
      }
      .job-type {
        cursor: pointer;
        margin-right: 15px;
      }
      .helper-text {
        color: #9ba3af;
        margin-top: 5px;
      }
    }

    .no-selected {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translateX(-50%) translateY(-50%);
    }
  }
  .edit-job-dialog .errorMsg-block {
    float: left;
    height: 32px;
    line-height: 32px;
    color: red;
  }
</style>
<template>
  <div class="edit-job-dialog">
    <dao-dialog
      class="eidt-dialog-main"
      :config="config"
      :visible.sync="isShow"
      @dao-dialog-open="handleEditOpen"
      @dao-dialog-close="handleEditClose"
    >
      <div class="edit-content-wrap">
        <div class="show-panel">
          <StyleTable :height="tableHeight" >
            <template slot="body" v-if="jobs.length>0" >
              <tr
                @click.prevent="onHandleSelectJob(index)"
                :class="{active: selectedJob === index}"
                :key="index"
                v-for="(job, index) in jobs">
                <td>
                  {{job.Name}}
                </td>
              </tr>
            </template>
          </StyleTable>
          <div class="jobs-btn-group">
            <span class="icon-btn" @click="addJob()">
              <svg class="icon">
                <use xlink:href="#icon_plus"></use>
              </svg>
            </span><!--
            --><span class="icon-btn" @click="openDeleteAlert()">
              <svg class="icon">
                <use xlink:href="#icon_status-dash"></use>
              </svg>
            </span><!--
            -->
         <!--    <label
              class="word-btn"
              for="jobs-upload">
              <input
                class="input-file"
                type="file"
                name="jobs-upload"
                id="jobs-upload"
                ref="importFileBtn"
                @change="onFileSelect">
              导入
            </label> -->
            <!--
            -->
           <!--  <span class="word-btn">
              导出
            </span> -->
          </div>
        </div>
        <div class="edit-panel">
          <span class="no-selected" v-if="selectedJob < 0">
            未选中作业
          </span>
          <div v-else>
            <div class="title">
              作业名称
            </div>
            <input
              type="text"
              class="dao-control"
              v-model.trim="jobs[selectedJob].Name"
              placeholder="名称"
              :disabled="jobType !== 'others'"
              />
            <p class="helper-text">
              1 - 10 字，作业名不可重复
            </p>
            <div>
              <label  class="job-type">
                <input type="radio" name="jobType" value="up" v-model="jobType" @change="jobs[selectedJob].Name = 'up'" /> 启动作业
              </label>
              <label  class="job-type">
                <input type="radio" name="jobType" value="down" v-model="jobType" @change="jobs[selectedJob].Name = 'down'" /> 回收作业
              </label>
              <label  class="job-type">
                <input type="radio" name="jobType" value="others" v-model="jobType" /> 其他
              </label>
            </div>
            <div class="title">
              命令
            </div>
            <textarea
              class="dao-control"
              type="text"
              rows="3"
              :placeholder="placeholder"
              v-model="jobs[selectedJob].Cmd" />
            <p class="helper-text">
              必填, 最多 4096 个字符
            </p>
            <div class="title">
              执行用户
            </div>
            <input
              type="text"
              class="dao-control"
              v-model.trim="jobs[selectedJob].User"
              placeholder="默认 root (可选)"
              />
            <p class="helper-text">
              0-31 字符，小写字母、数字、_。以 小写字母 或 _ 开头。
            </p>
          </div>
        </div>
      </div>
      <div slot="footer">
        <div class="errorMsg-block" v-if="isStartCheck && !checkAllOk()">
          {{errorMsg}}
        </div>
        <button class="dao-btn ghost"
          :disabled="isAllReadySave"
          @click="cancel()">取消</button>
        <button
          class="dao-btn blue"
          :disabled="!checkAllOk() || isAllReadySave"
          @click="save()">保存</button>
      </div>
    </dao-dialog>
    <dao-dialog
      v-if="isDeleteShow"
      class="deleteDialog"
      :visible.sync="isDeleteShow"
      :config="deletConfig"
    >
      <div class="edit-content-wrap">
        你确定要删除此作业么?
      </div>
        <div slot="footer">
          <button class="dao-btn red"
            :disabled="isAllReadyDelete"
            @click="handleDeleteConfirm()">删除</button>
          <button class="dao-btn ghost"
            :disabled="isAllReadyDelete"
            @click="handleDeleteCancel()">取消</button>
        </div>
      </dao-dialog>
    </dao-dialog>
  </div>
</template>
<script>
import Utils from '../../utils/index';
import StyleTable from '../styleTable/StyleTable';
import ApiService from '../../common/apiService';
import StyleTableAction from '../styleTable/StyleTableAction';

export default {
  name: 'EditJobDialog',
  props: {
    visible: {
      type: Boolean,
      require: true,
      default: false,
    },
    jobList: Array,
    appName: String,
  },
  data() {
    return {
      tableHeight: 12,
      config: {
        type: 'normal',
        title: '配置作业',
        showHeader: true,
        showFooter: true,
        closeOnClickOutside: true,
        closeOnPressEscape: true,
      },
      isShow: this.visible,
      selectedJob: -1,
      selectFile: null,
      // delete 弹窗
      isDeleteShow: false,
      deletConfig: {
        type: 'normal',
        title: '删除作业',
        size: 'sm',
      },
      cacheJobs: [],
      shouldReduceJobs: [],
      /* eslint-disable quotes   */
      placeholder: `例如: sh -c "sleep 1 && echo 'DCE jobs'"`,
      errorMsg: '作业名称不能重复',
      jobs: this.jobList ? StyleTableAction.init(this.jobList, this.tableHeight) : [],
      // 是否已经点击过 save
      isAllReadySave: false,
      // 是否已经点击过 删除
      isAllReadyDelete: false,
      // 开始检测
      isStartCheck: false,
      // 作业类型
      jobType: 'others',
    };
  },
  computed: {
  },
  methods: {
    handleEditOpen() {
      this.isStartCheck = true;
    },
    // delete
    openDeleteAlert() {
      if (!this.jobs[this.selectedJob]) return;
      if (!this.jobs[this.selectedJob].JobId) {
        this.reduceJob(this.selectedJob);
      } else {
        this.isDeleteShow = true;
      }
    },
    handleDeleteConfirm() {
      this.isAllReadyDelete = true;
      if (!this.jobs[this.selectedJob].JobId) {
        this.reduceJob(this.selectedJob);
      } else {
        this.pretendReduceJob(this.selectedJob);
      }
    },
    handleDeleteCancel() {
      this.isDeleteShow = false;
    },
    // 本个 dialog
    cancel() {
      this.close();
    },
    save() {
      if (!this.checkAllOk()) {
        Utils.createNoty(this.errorMsg, 'error');
        return;
      }
      this.isAllReadySave = true;

      const promiseLists = [];

      this.jobs.forEach((item, idx) => {
        if (!item) return;
        promiseLists.push(this.handleJob(item, idx));
      });

      this.shouldReduceJobs.forEach((item) => {
        if (!item.JobId) return;
        const reduceJobPromise = this.reduceJobService(item)
          .then((res) => {
            const index = this.cacheJobs.findIndex(job => job.JobId === item.JobId);
            if (index > -1) {
              this.cacheJobs.splice(index, 1);
            }
            return res;
          });
        promiseLists.push(
          reduceJobPromise);
      });

      Promise.all(promiseLists)
        .then(() => {
          // console.log('cacheJobs', this.getCurJobs
          this.close();
          this.isAllReadySave = false;
          Utils.createNoty('任务保存成功!', 'success');
        }, (error) => {
          this.isAllReadySave = false;
          Utils.createNoty(`${(error.body.id && error.body.id === 'jobs_name_duplicated_error') ? '作业名称重复' : '任务保存失败'}, 请重试!`, 'error');
          console.error('任务保存失败', error);
        });
    },
    handleJob(job, index) {
      if (job.JobId) {
        if (!this.detectJobChange(job, index)) return false;

        const { JobId, ...data } = job;

        if (!data.AppName) {
          if (!this.appName) {
            this.appName = this.getAppName();
          }
          data.AppName = this.appName;
        }

        return ApiService
          .putJobs(job.JobId, data)
          .then((res) => {
            this.jobs[index] = res;
            // 更新 cache
            this.cacheJobs[index] = res;
            return res;
          });
      }
      return ApiService
        .createJobs(job)
        .then((res) => {
          this.jobs[index] = res;

          // 更新 cache
          this.cacheJobs[index] = res;
          return res;
        });
    },
    close() {
      this.isShow = false;
    },
    handleEditClose() {
      this.isStartCheck = false;
      this.selectedJob = -1;
      this.isErrorShow = false;
      this.shouldReduceJobs = [];
      this.$emit('update:jobList', this.getCurJobs());
      // this.$emit('closeEditJob', this.getCurJobs());
      this.cacheJobs = [];
    },
    onHandleSelectJob(index) {
      if (!this.jobs[index]) return;
      this.selectedJob = index;
      const jobName = this.jobs[index].Name;
      if (jobName === 'down') {
        this.jobType = 'down';
      } else if (jobName === 'up') {
        this.jobType = 'up';
      } else {
        this.jobType = 'others';
      }
    },
    addJob() {
      const relaLength = this.detectJobLength();
      this.jobType = 'others';
      /* eslint-disable no-lonely-if */
      if (this.jobs.length > this.tableHeight || relaLength === this.tableHeight) {
        this.jobs.push(this.creatAJob());
      } else if (this.jobs.length === 0) {
        const tempA = [];
        tempA.push(this.creatAJob());
        this.jobs = StyleTableAction.init(tempA, this.tableHeight);
      } else {
        // this.jobs[relaLength] = this.creatAJob();
        // 上面这样是无法监控 新加入的 object
        this.$set(this.jobs, relaLength, this.creatAJob());
      }
      this.selectedJob = relaLength;
      this.$forceUpdate();
    },
    pretendReduceJob(index) {
      // 假删
      this.shouldReduceJobs.push(this.jobs[index]);
      this.reduceSelect(index);
      this.jobs.splice(index, 1);
      if (this.jobs.length < this.tableHeight) {
        this.jobs.push(0);
      }
      this.isAllReadyDelete = false;
      this.isDeleteShow = false;
      this.$forceUpdate();
    },
    reduceJob(index) {
      if (this.jobs[index].JobId) {
        // ApiService.deleteJobs(this.jobs[index].JobId)
        this.reduceJobService(this.jobs[index])
          .then(() => {
            this.reduceSelect(index);
            this.jobs.splice(index, 1);
            // cache 删除
            this.cacheJobs.splice(index, 1);
            if (this.jobs.length < this.tableHeight) {
              this.jobs.push(0);
            }
            this.isAllReadyDelete = false;
            this.isDeleteShow = false;
          });
      } else {
        this.reduceSelect(index);
        this.jobs.splice(index, 1);
        if (this.jobs.length < this.tableHeight) {
          this.jobs.push(0);
        }
        this.isAllReadyDelete = false;
        this.$forceUpdate();
      }
    },
    reduceJobService(job) {
      if (!job.JobId) return false;
      return ApiService.deleteJobs(job.JobId);
    },
    // reduceJob(index) {
    //   ApiService.deleteJobs(this.jobs[index].JobId)
    //     .then(() => {
    //       this.reduceSelect(index);
    //       this.jobs.splice(index, 1);
    //       // cache 删除
    //       this.cacheJobs.splice(index, 1);
    //       if (this.jobs.length < this.tableHeight) {
    //         this.jobs.push(0);
    //       }
    //       this.isAllReadyDelete = false;
    //       this.isDeleteShow = false;
    //     });
    // },
    reduceSelect(index) {
      if (index === 0) {
        if (!this.jobs[index + 1]) {
          this.selectedJob = -1;
        }
      } else if (!this.jobs[index + 1]) {
        this.selectedJob = index - 1;
      }
    },
    /* eslint-disable */
    // 导入导出部分
    // content-type text/plain
    onFileSelect() {
      const importE = this.$refs.importFileBtn;
      // console.log(importE.files[0]);
      this.uploadFile = importE.files[0];
      // if (this.selectFile.file.name.slice(-4) !== '.csv') return;
      if (typeof(FileReader) !== 'undefined') {
        let reader = new window.FileReader()
        reader.readAsText(importE.files[0]);
        reader.onload = function (e) {
          const data = e.target.result;
          // console.log(data);
        }
      }
    },
    // service
    getJobs() {
      return ApiService.getJobs();
    },
    // 工具类
    creatAJob() {
      if (!this.appName) {
        this.appName = this.getAppName();
      }

      return {
        Name: '未命名作业',
        Cmd: null,
        User: null,
        Privileged: true,
        secretArgs: [],
        Env: [],
        ServiceName: '',
        AppName: this.appName,
      };
    },
    detectJobLength() {
      const idx = this.jobs.indexOf(0);
      if (idx >= 0 && idx <= this.tableHeight - 1) {
        return idx;
      }
      return this.jobs.length;
    },
    // get App Name
    getAppName() {
      const queryList = window.location.search.substr(1).split('&');
      const nameQuery = queryList.filter(query => query.startsWith('ObjectId'));
      if (nameQuery[0]) {
        return nameQuery[0].split('=')[1];
      }
      return false;
    },
    getCurJobs() {
      return this.cacheJobs.filter((item) => item && item.JobId);
    },
    detectJobChange(newJob, index) {
      const { Name, User, Cmd } = newJob;
      const { Name: oName, User: oUser, Cmd: oCmd } = this.cacheJobs[index];
      return Name !== oName || User !== oUser || Cmd !== oCmd;
    },
    // 检测名称重复，是否全部填完
    checkAllOk() {
      if (!this.isStartCheck) return;

      let dupContainer = {};
      return this.jobs.every((item, idx) => {
        if (!item) return true;
        if (!dupContainer[item.Name]) {
          dupContainer[item.Name] = 1;
          // 检测是否全部填完
          return this.checkJobOk(item);
        }
        this.errorMsg = '作业名称不能重复';
        return false;
      });
    },
    // 单个的检查
    checkJobOk(job) {
      const { Name, Cmd, User } = job;
      // TODO Name 长度
      const nameMax = 10;
      const cmdMax = 4096;
      // Name, Cmd 是否为空
      if (!this.checkIsEmpty(Name) || !this.checkIsEmpty(Cmd)){
        this.errorMsg = '作业名称，命令不能为空';
        return false;
      };
      // Name  超过长度
      if (Name.length > nameMax) {
        this.errorMsg = '作业名称字数不能超过 10';
        return false;
      };

      if (Cmd.length > cmdMax) {
        this.errorMsg = '命令字数不能超过 4096';
        return false;
      };

      // 如果有执行用户的话，执行用户限制： ([a-z_][a-z0-9_]{0,30})
      // 以 小写字母 ／ _ 开头， 小写字母 ／ 数字 ／ _  在 0 - 31 个字符内
      if (User) {
        const reg = /^[a-z_][a-z0-9_]{0,30}$/g;
        if (!reg.test(User)) {
          this.errorMsg = '执行用户必须 以小写字母或 _ 开头，只能输入小写字母或数字或 _ ，总数不超过 31 个字符';
          return false;
        }
      }
      return true;
    },
    checkIsEmpty(item) {
      const toString = Object.prototype.toString;
      // 判断 null, undefined
      if (toString.call(item) === '[object Undefined]' || toString.call(item) === '[object Null]' || item === '') {
        return false;
      }

      return true;
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
    jobList(newV, oldV) {
      if (!newV) return;
      const len = newV.length;
      /* eslint-disable no-plusplus */
      // 为了不只是 浅拷贝
      this.cacheJobs = [];
      newV.forEach((item) => {
        this.cacheJobs.push({
          ...item,
        });
      });
      this.jobs = StyleTableAction.init(this.jobList, this.tableHeight) || [];
    },
  },
  components: {
    StyleTable,
  },
};
</script>
