"use strict";
(self["webpackChunkvdk_jupyterlab_extension"] = self["webpackChunkvdk_jupyterlab_extension"] || []).push([["lib_commandsAndMenu_js-lib_index_js"],{

/***/ "./lib/commandsAndMenu.js":
/*!********************************!*\
  !*** ./lib/commandsAndMenu.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   runningVdkOperation: () => (/* binding */ runningVdkOperation),
/* harmony export */   updateVDKMenu: () => (/* binding */ updateVDKMenu)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _components_RunJob__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./components/RunJob */ "./lib/components/RunJob.js");
/* harmony import */ var _jobData__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./jobData */ "./lib/jobData.js");
/* harmony import */ var _components_DeployJob__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./components/DeployJob */ "./lib/components/DeployJob.js");
/* harmony import */ var _components_CreateJob__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./components/CreateJob */ "./lib/components/CreateJob.js");
/* harmony import */ var _components_DownloadJob__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./components/DownloadJob */ "./lib/components/DownloadJob.js");
/* harmony import */ var _components_ConvertJobToNotebook__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./components/ConvertJobToNotebook */ "./lib/components/ConvertJobToNotebook.js");
/* harmony import */ var _serverRequests__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./serverRequests */ "./lib/serverRequests.js");
/* harmony import */ var _vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./vdkOptions/vdk_options */ "./lib/vdkOptions/vdk_options.js");
/* harmony import */ var ___WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! . */ "./lib/index.js");










var runningVdkOperation = '';
function updateVDKMenu(commands, docManager, fileBrowser, notebookTracker, statusButton) {
    // Add Run job command
    add_command(commands, 'jp-vdk:menu-run', 'Run', 'Execute VDK Run Command', _components_RunJob__WEBPACK_IMPORTED_MODULE_1__.showRunJobDialog, statusButton, docManager);
    // Add Create job command
    add_command(commands, 'jp-vdk:menu-create', 'Create', 'Execute VDK Create Command', _components_CreateJob__WEBPACK_IMPORTED_MODULE_2__.showCreateJobDialog, statusButton);
    // Add Download job command
    add_command(commands, 'jp-vdk:menu-download', 'Download', 'Execute VDK Download Command', _components_DownloadJob__WEBPACK_IMPORTED_MODULE_3__.showDownloadJobDialog, statusButton);
    // Add Convert Job To Notebook command
    add_command(commands, 'jp-vdk:menu-convert-job-to-notebook', 'Convert Job To Notebook', 'Convert Data Job To Jupyter Notebook', _components_ConvertJobToNotebook__WEBPACK_IMPORTED_MODULE_4__.showConvertJobToNotebookDialog, statusButton, undefined, fileBrowser, notebookTracker);
    // Add Create Deployment command
    add_command(commands, 'jp-vdk:menu-create-deployment', 'Deploy', 'Create deployment of a VDK job', _components_DeployJob__WEBPACK_IMPORTED_MODULE_5__.showCreateDeploymentDialog, statusButton);
}
/**
 *@param schemaNaming - string representing the command in the schema in schema/plugin.json
 *@param label - the label that will be added in the Menu
 *@param caption - the caption for the command.
 *@param getOperationDialog - function that will load the dialog for the command
 */
function add_command(commands, schemaNaming, label, caption, getOperationDialog, statusButton, docManager, fileBrowser, notebookTracker) {
    commands.addCommand(schemaNaming, {
        label: label,
        caption: caption,
        execute: async () => {
            try {
                if (!runningVdkOperation) {
                    runningVdkOperation = schemaNaming;
                    _jobData__WEBPACK_IMPORTED_MODULE_6__.jobData.set(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_7__.VdkOption.PATH, ___WEBPACK_IMPORTED_MODULE_8__.workingDirectory);
                    await (0,_serverRequests__WEBPACK_IMPORTED_MODULE_9__.jobdDataRequest)();
                    if (label === 'Convert Job To Notebook') {
                        await getOperationDialog(commands, fileBrowser, notebookTracker, statusButton);
                    }
                    else if (docManager) {
                        await getOperationDialog(docManager, statusButton);
                    }
                    else {
                        await getOperationDialog(statusButton);
                    }
                    statusButton.hide();
                    (0,_jobData__WEBPACK_IMPORTED_MODULE_6__.setJobDataToDefault)();
                    runningVdkOperation = '';
                }
                else {
                    await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)('Another VDK operation is currently running!', 'Please wait until the operation ends!', [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton()]);
                }
            }
            catch (error) {
                await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)('Encountered an error when trying to open the dialog. Error:', error, [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton()]);
            }
        }
    });
}


/***/ }),

/***/ "./lib/components/ConvertJobToNotebook.js":
/*!************************************************!*\
  !*** ./lib/components/ConvertJobToNotebook.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   createTranformedNotebook: () => (/* binding */ createTranformedNotebook),
/* harmony export */   "default": () => (/* binding */ ConvertJobToNotebookDialog),
/* harmony export */   initializeNotebookContent: () => (/* binding */ initializeNotebookContent),
/* harmony export */   notebookContent: () => (/* binding */ notebookContent),
/* harmony export */   populateNotebook: () => (/* binding */ populateNotebook),
/* harmony export */   showConvertJobToNotebookDialog: () => (/* binding */ showConvertJobToNotebookDialog)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jobData__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../jobData */ "./lib/jobData.js");
/* harmony import */ var _vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../vdkOptions/vdk_options */ "./lib/vdkOptions/vdk_options.js");
/* harmony import */ var _VdkTextInput__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./VdkTextInput */ "./lib/components/VdkTextInput.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _serverRequests__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../serverRequests */ "./lib/serverRequests.js");
/* harmony import */ var _VdkErrorMessage__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./VdkErrorMessage */ "./lib/components/VdkErrorMessage.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../utils */ "./lib/utils.js");








var notebookContent;
/**
 * A class responsible for the Transform Job operation
 * for more information check:
 * https://github.com/vmware/versatile-data-kit/wiki/VDK-Jupyter-Integration-Convert-Job-Operation
 */
class ConvertJobToNotebookDialog extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    /**
     * Returns a React component for rendering a convert menu.
     *
     * @param props - component properties
     * @returns React component
     */
    constructor(props) {
        super(props);
    }
    /**
     * Renders a dialog for converting a data job.
     *
     * @returns React element
     */
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_VdkTextInput__WEBPACK_IMPORTED_MODULE_2__["default"], { option: _vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__.VdkOption.PATH, value: this.props.jobPath, label: "Path to job directory:" })));
    }
}
async function showConvertJobToNotebookDialog(commands, fileBrowser, notebookTracker, statusButton) {
    const result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
        title: _utils__WEBPACK_IMPORTED_MODULE_4__.CONVERT_JOB_TO_NOTEBOOK_BUTTON_LABEL,
        body: (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(ConvertJobToNotebookDialog, { jobPath: _jobData__WEBPACK_IMPORTED_MODULE_5__.jobData.get(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__.VdkOption.PATH) })),
        buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton(), _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton()]
    });
    if (result.button.accept) {
        const confirmation = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
            title: _utils__WEBPACK_IMPORTED_MODULE_4__.CONVERT_JOB_TO_NOTEBOOK_BUTTON_LABEL,
            body: (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null,
                "Are you sure you want to convert the Data Job with path:",
                ' ',
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("i", null, _jobData__WEBPACK_IMPORTED_MODULE_5__.jobData.get(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__.VdkOption.PATH)),
                " to notebook?")),
            buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton(), _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton()]
        });
        if (confirmation.button.accept) {
            statusButton === null || statusButton === void 0 ? void 0 : statusButton.show('Convert', _jobData__WEBPACK_IMPORTED_MODULE_5__.jobData.get(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__.VdkOption.PATH));
            let { message, status } = await (0,_serverRequests__WEBPACK_IMPORTED_MODULE_6__.jobConvertToNotebookRequest)();
            if (status) {
                const transformjobResult = JSON.parse(message);
                notebookContent = initializeNotebookContent(transformjobResult['code_structure'], transformjobResult['removed_files']);
                await createTranformedNotebook(commands, fileBrowser, notebookTracker);
                await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                    title: _utils__WEBPACK_IMPORTED_MODULE_4__.CONVERT_JOB_TO_NOTEBOOK_BUTTON_LABEL,
                    body: (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "vdk-convert-to-notebook-dialog-message-container" },
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", { className: "vdk-convert-to-notebook-dialog-message" },
                            "The Data Job with path ",
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("i", null, _jobData__WEBPACK_IMPORTED_MODULE_5__.jobData.get(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__.VdkOption.PATH)),
                            " was converted to notebook successfully!"))),
                    buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton()]
                });
            }
            else {
                if (message) {
                    message = 'ERROR : ' + message;
                    const errorMessage = new _VdkErrorMessage__WEBPACK_IMPORTED_MODULE_7__.VdkErrorMessage(message);
                    await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                        title: _utils__WEBPACK_IMPORTED_MODULE_4__.CONVERT_JOB_TO_NOTEBOOK_BUTTON_LABEL,
                        body: (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "vdk-convert-to-notebook-error-message " },
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null, errorMessage.exception_message),
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null, errorMessage.what_happened),
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null, errorMessage.why_it_happened),
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null, errorMessage.consequences),
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null, errorMessage.countermeasures))),
                        buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton()]
                    });
                }
            }
        }
    }
}
/**
 * Create a notebook for a transformed job.
 *
 * The function navigates to the job directory and creates a new notebook
 * file. The notebook is then populated with the content provided as parameter.
 *
 * @param {JupyterCellProps[]} notebookContent - The content to populate the notebook with.
 * @param {CommandRegistry} commands - The command registry to execute Jupyter commands.
 * @param {FileBrowser} fileBrowser - The file browser to navigate the file system.
 * @param {INotebookTracker} notebookTracker - The notebook tracker to track changes to the notebook.
 */
const createTranformedNotebook = async (commands, fileBrowser, notebookTracker) => {
    try {
        const baseDir = await (0,_serverRequests__WEBPACK_IMPORTED_MODULE_6__.getServerDirRequest)();
        _jobData__WEBPACK_IMPORTED_MODULE_5__.jobData.set(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__.VdkOption.NAME, _jobData__WEBPACK_IMPORTED_MODULE_5__.jobData.get(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__.VdkOption.PATH).split(/[\\/]/).pop() || ''); //get the name of the job using the directory
        await fileBrowser.model.cd(_jobData__WEBPACK_IMPORTED_MODULE_5__.jobData.get(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__.VdkOption.PATH).substring(baseDir.length)); // relative path for Jupyter
        commands.execute('notebook:create-new');
    }
    catch (error) {
        await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showErrorMessage)('Something went wrong while trying to create the new transformed notebook. Error:', error, [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton()]);
    }
};
/**
 * Initializes notebook content.
 *
 * The function takes code and filenames as parameters and generates a structured notebook content.
 * The code blocks are turned into notebook cells.
 *
 * @param {string[]} codeStructure - The code blocks to turn into notebook cells.
 * @param {string[]} fileNames - The names of the files to turn into titles.
 * @return {JupyterCellProps[]} - The structured content ready to be used to populate a notebook.
 */
const initializeNotebookContent = (codeStructure, fileNames) => {
    const notebookContent = [];
    for (let i = 0; i < codeStructure.length; i++) {
        notebookContent.push({
            source: '#### ' + fileNames[i],
            type: 'markdown'
        });
        notebookContent.push({
            source: codeStructure[i],
            type: 'code'
        });
        if (codeStructure[i].includes('def run(job_input: IJobInput)')) {
            notebookContent.push({
                source: 'run(job_input)',
                type: 'code'
            });
        }
    }
    return notebookContent;
};
/**
 * Populates notebook with provided content.
 *
 * The function takes notebook content and a notebook tracker as parameters.
 * When a new notebook becomes active, it is populated with the provided content.
 * @param {INotebookTracker} notebookTracker - The notebook tracker to track changes to the notebook.
 */
const populateNotebook = async (notebookTracker) => {
    var _a, _b;
    const notebookPanel = notebookTracker.currentWidget;
    if (notebookPanel) {
        const cells = (_b = (_a = notebookTracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content.model) === null || _b === void 0 ? void 0 : _b.cells;
        const cellContent = cells === null || cells === void 0 ? void 0 : cells.get(0).value.text;
        // check if the notebook has only 1 empty cell, which is how we judge if it is a new notebook or not
        if (cells && cells.length <= 1 && cellContent == '') {
            cells.remove(1);
            const addMarkdownCell = (source) => {
                var _a, _b;
                const markdownCell = (_b = (_a = notebookPanel.content.model) === null || _a === void 0 ? void 0 : _a.contentFactory) === null || _b === void 0 ? void 0 : _b.createMarkdownCell({
                    cell: {
                        cell_type: 'markdown',
                        source: source,
                        metadata: {}
                    }
                });
                if (markdownCell) {
                    cells.push(markdownCell);
                }
            };
            const addCodeCell = (source, metadata) => {
                var _a, _b;
                const codeCell = (_b = (_a = notebookPanel.content.model) === null || _a === void 0 ? void 0 : _a.contentFactory) === null || _b === void 0 ? void 0 : _b.createCodeCell({
                    cell: {
                        cell_type: 'code',
                        source: source,
                        metadata: metadata
                    }
                });
                if (codeCell) {
                    cells.push(codeCell);
                }
            };
            addMarkdownCell(['# ' + _jobData__WEBPACK_IMPORTED_MODULE_5__.jobData.get(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__.VdkOption.NAME)]);
            addMarkdownCell([
                '### Please go through this guide before continuing with the data job run and development.'
            ]);
            addMarkdownCell([
                '#### Introduction and Preparations\n',
                '*  *This is a notebook transformed from a directory style data job located in ' +
                    _jobData__WEBPACK_IMPORTED_MODULE_5__.jobData.get(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__.VdkOption.PATH) +
                    '.*\n',
                '*  *If you are not familiar with notebook data jobs make sure to check the **Getting Started**(TODO: add link) page.*\n',
                '*  *You can find the **original job** at ' +
                    _jobData__WEBPACK_IMPORTED_MODULE_5__.jobData.get(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__.VdkOption.PATH).split(/[/\\]/).slice(0, -1).join('/') +
                    '.*'
            ]);
            addMarkdownCell([
                '#### Execution Order and Identifying Cells\n',
                '*  *The below cells are automatically generated corresponding to a step(.sql or .py file with VDK run function) \n',
                '    in your original job.* \n',
                '*  *You will notice that some cells are coloured and include the VDK logo and a numbering. \n',
                '    These are the "vdk" tagged cells.\n',
                '    Only these cells are executed during VDK run and all the others are ignored(for example the current cell).*\n',
                '*  *Code cells in the notebook will be executed according to the numbering when running the notebook data job with VDK.\n',
                '    This means that the steps in the job are organized from the top to the bottom, starting with the first step.*\n',
                '*  *When you see a title saying **"Step generated from: sample.py"** before some blocks of code, \n',
                '    it means that the code below that title was created from the "sample.py" file.*\n',
                '*  *Similarly, if you come across code cells that have the format **"job_input.execute_query(query_string)"** ,\n',
                '    it means that those cells contain code generated from ".sql" files.*\n',
                '*  *On the other hand, code cells originating from ".py" files remain unchanged.\n',
                '    However, an additional cell is included that calls the "run" function using the command **"run(job_input)"** . \n',
                '    This cell executes the "run" function from the code generated from the ".py" file.*\n',
                '*  *You can delete the cells that are not tagged with "vdk" \n',
                "    as they are not essential to the data job's execution.\n",
                '    However, removing tagged cells will result in a different data job run.* '
            ]);
            addMarkdownCell([
                '#### Tips: \n',
                '* *Before running the job, it is recommended to review the cells\n',
                '    to ensure a clear understanding of the data job run.  \n',
                '    This will help to ensure the desired outcome.* '
            ]);
            addCodeCell([
                '"""\n',
                'vdk.plugin.ipython extension introduces a magic command for Jupyter.\n',
                'The command enables the user to load VDK for the current notebook.\n',
                'VDK provides the job_input API, which has methods for:\n',
                '    * executing queries to an OLAP database;\n',
                '    * ingesting data into a database;\n',
                '    * processing data into a database.\n',
                'See the IJobInput documentation for more details.\n',
                'https://github.com/vmware/versatile-data-kit/blob/main/projects/vdk-core/src/vdk/api/job_input.py\n',
                'Please refrain from tagging this cell with VDK as it is not an actual part of the data job\n',
                'and is only used for development purposes.\n',
                '"""\n',
                '%reload_ext vdk.plugin.ipython\n',
                '%reload_VDK\n',
                'job_input = VDK.get_initialized_job_input()'
            ], {});
            // add code that came from the previous version of the job and the names of the files where they came from
            for (const cellProps of notebookContent) {
                if (cellProps.type === 'markdown') {
                    addMarkdownCell([cellProps.source]);
                }
                else if (cellProps.type === 'code') {
                    addCodeCell([cellProps.source], {
                        tags: ['vdk']
                    });
                }
            }
            notebookContent = [];
        }
    }
};


/***/ }),

/***/ "./lib/components/CreateJob.js":
/*!*************************************!*\
  !*** ./lib/components/CreateJob.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ CreateJobDialog),
/* harmony export */   showCreateJobDialog: () => (/* binding */ showCreateJobDialog)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jobData__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../jobData */ "./lib/jobData.js");
/* harmony import */ var _vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../vdkOptions/vdk_options */ "./lib/vdkOptions/vdk_options.js");
/* harmony import */ var _VdkTextInput__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./VdkTextInput */ "./lib/components/VdkTextInput.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _serverRequests__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../serverRequests */ "./lib/serverRequests.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../utils */ "./lib/utils.js");







class CreateJobDialog extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    /**
     * Returns a React component for rendering a create menu.
     *
     * @param props - component properties
     * @returns React component
     */
    constructor(props) {
        super(props);
    }
    /**
     * Renders a dialog for creating a data job.
     *
     * @returns React element
     */
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_VdkTextInput__WEBPACK_IMPORTED_MODULE_2__["default"], { option: _vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__.VdkOption.NAME, value: this.props.jobName, label: "Job Name:" }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_VdkTextInput__WEBPACK_IMPORTED_MODULE_2__["default"], { option: _vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__.VdkOption.TEAM, value: this.props.jobTeam, label: "Job Team:" }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_VdkTextInput__WEBPACK_IMPORTED_MODULE_2__["default"], { option: _vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__.VdkOption.PATH, value: this.props.jobPath, label: "Path to job directory:" })));
    }
}
async function showCreateJobDialog() {
    const result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
        title: _utils__WEBPACK_IMPORTED_MODULE_4__.CREATE_JOB_BUTTON_LABEL,
        body: (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(CreateJobDialog, { jobPath: _jobData__WEBPACK_IMPORTED_MODULE_5__.jobData.get(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__.VdkOption.PATH), jobName: _jobData__WEBPACK_IMPORTED_MODULE_5__.jobData.get(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__.VdkOption.NAME), jobTeam: _jobData__WEBPACK_IMPORTED_MODULE_5__.jobData.get(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__.VdkOption.TEAM) })),
        buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton(), _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton()]
    });
    if (result.button.accept) {
        await (0,_serverRequests__WEBPACK_IMPORTED_MODULE_6__.jobRequest)('create');
    }
}


/***/ }),

/***/ "./lib/components/DeployJob.js":
/*!*************************************!*\
  !*** ./lib/components/DeployJob.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ DeployJobDialog),
/* harmony export */   showCreateDeploymentDialog: () => (/* binding */ showCreateDeploymentDialog)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jobData__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../jobData */ "./lib/jobData.js");
/* harmony import */ var _vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../vdkOptions/vdk_options */ "./lib/vdkOptions/vdk_options.js");
/* harmony import */ var _VdkTextInput__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./VdkTextInput */ "./lib/components/VdkTextInput.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _serverRequests__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../serverRequests */ "./lib/serverRequests.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../utils */ "./lib/utils.js");







class DeployJobDialog extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    /**
     * Returns a React component for rendering a Deploy menu.
     *
     * @param props - component properties
     * @returns React component
     */
    constructor(props) {
        super(props);
    }
    /**
     * Renders a dialog for creating a new deployment of a Data Job.
     *
     * @returns React element
     */
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_VdkTextInput__WEBPACK_IMPORTED_MODULE_2__["default"], { option: _vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__.VdkOption.NAME, value: this.props.jobName, label: "Job Name:" }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_VdkTextInput__WEBPACK_IMPORTED_MODULE_2__["default"], { option: _vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__.VdkOption.TEAM, value: this.props.jobTeam, label: "Job Team:" }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_VdkTextInput__WEBPACK_IMPORTED_MODULE_2__["default"], { option: _vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__.VdkOption.PATH, value: this.props.jobPath, label: "Path to job directory:" }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_VdkTextInput__WEBPACK_IMPORTED_MODULE_2__["default"], { option: _vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__.VdkOption.DEPLOYMENT_REASON, value: "reason", label: "Deployment reason:" })));
    }
}
async function showCreateDeploymentDialog(statusButton) {
    const result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
        title: _utils__WEBPACK_IMPORTED_MODULE_4__.CREATE_DEP_BUTTON_LABEL,
        body: (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(DeployJobDialog, { jobName: _jobData__WEBPACK_IMPORTED_MODULE_5__.jobData.get(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__.VdkOption.NAME), jobPath: _jobData__WEBPACK_IMPORTED_MODULE_5__.jobData.get(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__.VdkOption.PATH), jobTeam: _jobData__WEBPACK_IMPORTED_MODULE_5__.jobData.get(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__.VdkOption.TEAM) })),
        buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton(), _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton()]
    });
    const resultButtonClicked = !result.value && result.button.accept;
    if (resultButtonClicked) {
        try {
            const runConfirmationResult = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                title: _utils__WEBPACK_IMPORTED_MODULE_4__.CREATE_DEP_BUTTON_LABEL,
                body: 'The job will be executed once before deployment.',
                buttons: [
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton({ label: 'Cancel' }),
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: 'Continue' })
                ]
            });
            if (runConfirmationResult.button.accept) {
                statusButton === null || statusButton === void 0 ? void 0 : statusButton.show('Deploy', _jobData__WEBPACK_IMPORTED_MODULE_5__.jobData.get(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__.VdkOption.PATH));
                const { message, status } = await (0,_serverRequests__WEBPACK_IMPORTED_MODULE_6__.jobRunRequest)();
                if (status) {
                    if (await (0,_jobData__WEBPACK_IMPORTED_MODULE_5__.checkIfVdkOptionDataIsDefined)(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__.VdkOption.DEPLOYMENT_REASON)) {
                        await (0,_serverRequests__WEBPACK_IMPORTED_MODULE_6__.jobRequest)('deploy');
                    }
                }
                else {
                    await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showErrorMessage)('Encоuntered an error while running the job!', message, [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton()]);
                }
            }
        }
        catch (error) {
            await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showErrorMessage)('Encountered an error when deploying the job. Error:', error, [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton()]);
        }
    }
}


/***/ }),

/***/ "./lib/components/DownloadJob.js":
/*!***************************************!*\
  !*** ./lib/components/DownloadJob.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ DownloadJobDialog),
/* harmony export */   showDownloadJobDialog: () => (/* binding */ showDownloadJobDialog)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../vdkOptions/vdk_options */ "./lib/vdkOptions/vdk_options.js");
/* harmony import */ var _VdkTextInput__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./VdkTextInput */ "./lib/components/VdkTextInput.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _serverRequests__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../serverRequests */ "./lib/serverRequests.js");
/* harmony import */ var _jobData__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../jobData */ "./lib/jobData.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../utils */ "./lib/utils.js");







class DownloadJobDialog extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    /**
     * Returns a React component for rendering a download menu.
     *
     * @param props - component properties
     * @returns React component
     */
    constructor(props) {
        super(props);
    }
    /**
     * Renders a dialog for downloading a data job.
     *
     * @returns React element
     */
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_VdkTextInput__WEBPACK_IMPORTED_MODULE_2__["default"], { option: _vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__.VdkOption.NAME, value: "default-name", label: "Job Name:" }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_VdkTextInput__WEBPACK_IMPORTED_MODULE_2__["default"], { option: _vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__.VdkOption.TEAM, value: "default-team", label: "Job Team:" }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_VdkTextInput__WEBPACK_IMPORTED_MODULE_2__["default"], { option: _vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__.VdkOption.PATH, value: this.props.jobPath, label: "Path to job directory:" })));
    }
}
async function showDownloadJobDialog(statusButton) {
    const result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
        title: _utils__WEBPACK_IMPORTED_MODULE_4__.DOWNLOAD_JOB_BUTTON_LABEL,
        body: (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(DownloadJobDialog, { jobPath: _jobData__WEBPACK_IMPORTED_MODULE_5__.jobData.get(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__.VdkOption.PATH) })),
        buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton(), _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton()]
    });
    if (result.button.accept) {
        statusButton === null || statusButton === void 0 ? void 0 : statusButton.show('Download', _jobData__WEBPACK_IMPORTED_MODULE_5__.jobData.get(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__.VdkOption.PATH));
        await (0,_serverRequests__WEBPACK_IMPORTED_MODULE_6__.jobRequest)('download');
    }
}


/***/ }),

/***/ "./lib/components/RunJob.js":
/*!**********************************!*\
  !*** ./lib/components/RunJob.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ RunJobDialog),
/* harmony export */   findFailingCellId: () => (/* binding */ findFailingCellId),
/* harmony export */   findFailingCellInNotebookCells: () => (/* binding */ findFailingCellInNotebookCells),
/* harmony export */   getCellInputAreaPrompt: () => (/* binding */ getCellInputAreaPrompt),
/* harmony export */   handleErrorsProducedByNotebookCell: () => (/* binding */ handleErrorsProducedByNotebookCell),
/* harmony export */   showRunJobDialog: () => (/* binding */ showRunJobDialog)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jobData__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../jobData */ "./lib/jobData.js");
/* harmony import */ var _vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../vdkOptions/vdk_options */ "./lib/vdkOptions/vdk_options.js");
/* harmony import */ var _VdkTextInput__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./VdkTextInput */ "./lib/components/VdkTextInput.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _serverRequests__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../serverRequests */ "./lib/serverRequests.js");
/* harmony import */ var _VdkErrorMessage__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./VdkErrorMessage */ "./lib/components/VdkErrorMessage.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../utils */ "./lib/utils.js");








class RunJobDialog extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    /**
     * Returns a React component for rendering a run menu.
     *
     * @param props - component properties
     * @returns React component
     */
    constructor(props) {
        super(props);
        /**
         * Callback invoked upon  changing the args input
         *
         * @param event - event object
         */
        this._onArgsChange = (event) => {
            const element = event.currentTarget;
            let value = element.value;
            if (value && this._isJSON(value)) {
                _jobData__WEBPACK_IMPORTED_MODULE_2__.jobData.set(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__.VdkOption.ARGUMENTS, value);
            }
        };
        this._isJSON = (str) => {
            try {
                JSON.parse(str);
                return true;
            }
            catch (e) {
                return false;
            }
        };
    }
    /**
     * Renders a dialog for running a data job.
     *
     * @returns React element
     */
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_VdkTextInput__WEBPACK_IMPORTED_MODULE_4__["default"], { option: _vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__.VdkOption.PATH, value: this.props.jobPath, label: "Path to job directory:" }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jp-vdk-input-wrapper" },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("label", { className: "jp-vdk-label", htmlFor: "arguments" }, "Arguments:"),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { type: "text", id: "arguments", className: "jp-vdk-input", placeholder: '{"key": "value"}', onChange: this._onArgsChange })),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("ul", { id: "argumentsUl", className: "hidden" })));
    }
}
async function showRunJobDialog(docManager, statusButton) {
    const result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
        title: _utils__WEBPACK_IMPORTED_MODULE_5__.RUN_JOB_BUTTON_LABEL,
        body: react__WEBPACK_IMPORTED_MODULE_0___default().createElement(RunJobDialog, { jobPath: _jobData__WEBPACK_IMPORTED_MODULE_2__.jobData.get(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__.VdkOption.PATH) }),
        buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton(), _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton()]
    });
    if (result.button.accept) {
        statusButton === null || statusButton === void 0 ? void 0 : statusButton.show('Run', _jobData__WEBPACK_IMPORTED_MODULE_2__.jobData.get(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_3__.VdkOption.PATH));
        let { message, status } = await (0,_serverRequests__WEBPACK_IMPORTED_MODULE_6__.jobRunRequest)();
        if (status) {
            (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                title: _utils__WEBPACK_IMPORTED_MODULE_5__.RUN_JOB_BUTTON_LABEL,
                body: (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "vdk-run-dialog-message-container" },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", { className: "vdk-run-dialog-message" }, "The job was executed successfully!"))),
                buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton()]
            });
        }
        else {
            message = 'ERROR : ' + message;
            const errorMessage = new _VdkErrorMessage__WEBPACK_IMPORTED_MODULE_7__.VdkErrorMessage(message);
            if (!docManager ||
                !(await handleErrorsProducedByNotebookCell(errorMessage, docManager))) {
                (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                    title: _utils__WEBPACK_IMPORTED_MODULE_5__.RUN_JOB_BUTTON_LABEL,
                    body: (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "vdk-run-error-message " },
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null, errorMessage.exception_message),
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null, errorMessage.what_happened),
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null, errorMessage.why_it_happened),
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null, errorMessage.consequences),
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null, errorMessage.countermeasures))),
                    buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton()]
                });
            }
        }
    }
}
const findFailingCellId = (message) => {
    const regex = /cell_id:([0-9a-fA-F-]+)/;
    const match = message.match(regex);
    if (match)
        return match[1];
    return '';
};
/**
 * Returns a Element that is used for numerating cell executions on Jupyter (text with [] if not executed and  with [1], [2] if executed)
 * @param failingCell - parent cell of that element
 * @returns Element or undefined if the element could not be found
 */
const getCellInputAreaPrompt = (failingCell) => {
    const cellInputWrappers = failingCell.getElementsByClassName('jp-Cell-inputWrapper');
    for (let i = 0; i < cellInputWrappers.length; i++) {
        const cellAreas = cellInputWrappers[i].getElementsByClassName('jp-Cell-inputArea');
        if (cellAreas.length > 0) {
            const cellInputArea = cellAreas[0];
            const promptElements = cellInputArea.getElementsByClassName('jp-InputArea-prompt');
            if (promptElements.length > 0) {
                return promptElements[0];
            }
        }
    }
};
const switchToFailingCell = (failingCell) => {
    const prompt = getCellInputAreaPrompt(failingCell);
    prompt === null || prompt === void 0 ? void 0 : prompt.classList.add('jp-vdk-failing-cell-prompt');
    failingCell.scrollIntoView();
    failingCell.classList.add('jp-vdk-failing-cell');
    // Delete previous fail numbering
    const vdkFailingCellNums = Array.from(document.getElementsByClassName('jp-vdk-failing-cell-num'));
    vdkFailingCellNums.forEach(element => {
        element.classList.remove('jp-vdk-failing-cell-num');
        element.classList.add('jp-vdk-cell-num');
    });
};
const unmarkOldFailingCells = (cell) => {
    cell.classList.remove('jp-vdk-failing-cell');
    const cellPrompt = getCellInputAreaPrompt(cell);
    cellPrompt === null || cellPrompt === void 0 ? void 0 : cellPrompt.classList.remove('jp-vdk-failing-cell-prompt');
};
const findFailingCellInNotebookCells = async (element, failingCellIndex, nbPath) => {
    const cells = element.children;
    if (failingCellIndex > cells.length) {
        (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
            title: _utils__WEBPACK_IMPORTED_MODULE_5__.RUN_FAILED_BUTTON_LABEL,
            body: (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null, "Sorry, something went wrong while trying to find the failing cell!"),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null,
                    "Please, check the ",
                    nbPath,
                    " once more and try to run the job while the notebook is active!"))),
            buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton()]
        });
    }
    else {
        for (let i = 0; i < cells.length; i++) {
            i === failingCellIndex
                ? switchToFailingCell(cells[i])
                : unmarkOldFailingCells(cells[i]);
        }
    }
};
/**
 * Seperate handling for notebook errors - option for the user to navigate to the failing cell when error is produced
 */
const handleErrorsProducedByNotebookCell = async (message, docManager) => {
    const failingCellId = findFailingCellId(message.what_happened);
    if (failingCellId) {
        const { path: nbPath, cellIndex: failingCellIndex } = await (0,_serverRequests__WEBPACK_IMPORTED_MODULE_6__.getNotebookInfo)(failingCellId);
        if (nbPath) {
            const navigateToFailingCell = async () => {
                const notebook = docManager.openOrReveal(nbPath);
                if (notebook) {
                    await notebook.revealed; // wait until the DOM elements are fully loaded
                    const children = Array.from(notebook.node.children);
                    if (children) {
                        children.forEach(async (element) => {
                            if (element.classList.contains('jp-Notebook')) {
                                findFailingCellInNotebookCells(element, Number(failingCellIndex), nbPath);
                            }
                        });
                    }
                }
            };
            const result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                title: _utils__WEBPACK_IMPORTED_MODULE_5__.RUN_JOB_BUTTON_LABEL,
                body: (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "vdk-run-error-message " },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null, message.exception_message),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null, message.what_happened),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null, message.why_it_happened),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null, message.consequences),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null, message.countermeasures))),
                buttons: [
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: 'See failing cell' }),
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton()
                ]
            });
            if (result.button.accept) {
                await navigateToFailingCell();
            }
            return true;
        }
    }
    return false;
};


/***/ }),

/***/ "./lib/components/StatusButton.js":
/*!****************************************!*\
  !*** ./lib/components/StatusButton.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   StatusButton: () => (/* binding */ StatusButton),
/* harmony export */   createStatusButton: () => (/* binding */ createStatusButton),
/* harmony export */   createStatusMenu: () => (/* binding */ createStatusMenu)
/* harmony export */ });
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../utils */ "./lib/utils.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _vdkTags__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../vdkTags */ "./lib/vdkTags.js");





const formatSeconds = (s) => new Date(s * 1000).toISOString().substr(11, 8);
class StatusButton {
    constructor(commands) {
        this.buttonElement = document.createElement('button');
        this.buttonElement.id = _utils__WEBPACK_IMPORTED_MODULE_3__.STATUS_BUTTON_ID;
        this.buttonElement.className = _utils__WEBPACK_IMPORTED_MODULE_3__.STATUS_BUTTON_CLASS;
        const contentContainer = document.createElement('div');
        contentContainer.className = 'jp-vdk-status-button-content';
        (0,_vdkTags__WEBPACK_IMPORTED_MODULE_4__.addVdkLogo)(contentContainer);
        const timeElement = document.createElement('span');
        timeElement.innerHTML = '00:00:00';
        contentContainer.appendChild(timeElement);
        this.buttonElement.appendChild(contentContainer);
        this.buttonElement.onclick = () => {
            commands.execute(_utils__WEBPACK_IMPORTED_MODULE_3__.STATUS_BUTTON_COMMAND_ID, {
                operation: this.operation,
                path: this.jobPath
            });
        };
        this.buttonElement.title =
            'VDK operation is in progress. Click here for more info.';
        this.buttonElement.style.display = 'none';
        this.counter = 0;
    }
    get element() {
        return this.buttonElement;
    }
    show(operation, path) {
        this.operation = operation;
        this.jobPath = path;
        this.buttonElement.style.display = '';
        this.startTimer();
    }
    hide() {
        this.buttonElement.style.display = 'none';
        this.stopTimer();
    }
    startTimer() {
        this.counter = 0;
        this.timerId = window.setInterval(() => {
            this.counter++;
            const timeElement = this.buttonElement.querySelector('span');
            if (timeElement) {
                timeElement.innerHTML = `${formatSeconds(this.counter)}`;
            }
        }, 1000);
    }
    stopTimer() {
        if (this.timerId) {
            clearInterval(this.timerId);
            this.timerId = undefined;
        }
        const timeElement = this.buttonElement.querySelector('span');
        if (timeElement) {
            timeElement.innerHTML = '00:00:00';
        }
    }
}
function createStatusButton(commands) {
    return new StatusButton(commands);
}
function createStatusMenu(commands) {
    commands.addCommand(_utils__WEBPACK_IMPORTED_MODULE_3__.STATUS_BUTTON_COMMAND_ID, {
        label: _utils__WEBPACK_IMPORTED_MODULE_3__.STATUS_BUTTON_LABEL,
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.checkIcon,
        execute: async (args) => {
            const operation = args.operation || 'UNKNOWN';
            const path = args.path || 'UNKNOWN';
            await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                title: _utils__WEBPACK_IMPORTED_MODULE_3__.STATUS_BUTTON_LABEL,
                body: (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "vdk-status-dialog-message-container" },
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("p", { className: "vdk-status-dialog-message" },
                        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("b", null, operation),
                        " operation is currently running for job with path: ",
                        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("i", null, path),
                        "!"))),
                buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton()]
            });
        }
    });
}


/***/ }),

/***/ "./lib/components/VdkErrorMessage.js":
/*!*******************************************!*\
  !*** ./lib/components/VdkErrorMessage.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   VdkErrorMessage: () => (/* binding */ VdkErrorMessage)
/* harmony export */ });
/*
 * Copyright 2021-2023 VMware, Inc.
 * SPDX-License-Identifier: Apache-2.0
 */
/*
 * Class that represents VDK Error messages in the UI
 * Check projects/vdk-core/src/vdk/internal/core/errors.py too see more about VDK errors
 */
class VdkErrorMessage {
    constructor(message) {
        this.exception_message = '';
        this.what_happened = '';
        this.why_it_happened = '';
        this.consequences = '';
        this.countermeasures = '';
        this.__parse_message(message);
    }
    __parse_message(message) {
        const keys = [
            'exception_message',
            'what_happened',
            'why_it_happened',
            'consequences',
            'countermeasures'
        ];
        const delimiters = [
            'ERROR : ',
            'WHAT HAPPENED :',
            'WHY IT HAPPENED :',
            'CONSEQUENCES :',
            'COUNTERMEASURES :'
        ];
        const lines = message.split('\n');
        let keyIndex = 0;
        for (let i = 0; i < lines.length; i++) {
            const delimiterIndex = lines[i].indexOf(delimiters[keyIndex]);
            if (delimiterIndex !== -1) {
                this[keys[keyIndex]] =
                    delimiters[keyIndex] +
                        lines[i].substring(delimiterIndex + delimiters[keyIndex].length);
                keyIndex++;
                if (keyIndex === keys.length) {
                    break;
                }
            }
            else {
                this.exception_message = message;
            }
        }
    }
}


/***/ }),

/***/ "./lib/components/VdkTextInput.js":
/*!****************************************!*\
  !*** ./lib/components/VdkTextInput.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ VDKTextInput)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jobData__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../jobData */ "./lib/jobData.js");


/**
   * This function is used to be sure that placeholder text is not overflowing in case of long path
   * if the string that is given is not path it will return the same string
   * if it is a path it will return the last directory
   */
const getLastPartOfPath = (path) => {
    const pathParts = path.split(/(?=[/\\])/); // Lookahead assertion to keep delimiter
    return pathParts[pathParts.length - 1];
};
class VDKTextInput extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    /**
     * Returns a React component for rendering a div with input and value  for VDK Option.
     *
     * @param props - component properties
     * @returns React component
     */
    constructor(props) {
        super(props);
        /**
         * Callback invoked upon changing the input.
         *
         * @param event - event object
         */
        this.onInputChange = (event) => {
            const nameInput = event.currentTarget;
            let value = nameInput.value;
            if (!value)
                value = this.props.value;
            _jobData__WEBPACK_IMPORTED_MODULE_1__.jobData.set(this.props.option, value);
        };
    }
    /**
     * Renders a div with input and value  for VDK Option.
     *
     * @returns React element
     */
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jp-vdk-input-wrapper" },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("label", { className: "jp-vdk-label", htmlFor: this.props.option }, this.props.label),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { type: "text", id: this.props.option, className: "jp-vdk-input", placeholder: getLastPartOfPath(this.props.value), onChange: this.onInputChange }))));
    }
}


/***/ }),

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   requestAPI: () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);
/*
 * Copyright 2021-2023 VMware, Inc.
 * SPDX-License-Identifier: Apache-2.0
 */


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'vdk-jupyterlab-extension', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw error;
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return data;
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   workingDirectory: () => (/* binding */ workingDirectory)
/* harmony export */ });
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _commandsAndMenu__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./commandsAndMenu */ "./lib/commandsAndMenu.js");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _vdkTags__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./vdkTags */ "./lib/vdkTags.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/docmanager */ "webpack/sharing/consume/default/@jupyterlab/docmanager");
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _initVDKConfigCell__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./initVDKConfigCell */ "./lib/initVDKConfigCell.js");
/* harmony import */ var _components_ConvertJobToNotebook__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./components/ConvertJobToNotebook */ "./lib/components/ConvertJobToNotebook.js");
/* harmony import */ var _components_StatusButton__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./components/StatusButton */ "./lib/components/StatusButton.js");
/* harmony import */ var _tokenUpdate__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./tokenUpdate */ "./lib/tokenUpdate.js");
/*
 * Copyright 2021-2023 VMware, Inc.
 * SPDX-License-Identifier: Apache-2.0
 */











/**
 * Current working directory in Jupyter
 * The variable can be accessed anywhere in the JupyterFrontEndPlugin
 */
let workingDirectory = '';
/**
 * Initialization data for the vdk-jupyterlab-extension extension.
 */
const plugin = {
    id: 'vdk-jupyterlab-extension:plugin',
    autoStart: true,
    optional: [
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__.ISettingRegistry,
        _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__.IFileBrowserFactory,
        _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__.INotebookTracker,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__.IThemeManager,
        _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_4__.IDocumentManager
    ],
    activate: async (app, settingRegistry, factory, notebookTracker, themeManager, docManager) => {
        const { commands } = app;
        notebookTracker.activeCellChanged.connect((sender, args) => {
            if (_commandsAndMenu__WEBPACK_IMPORTED_MODULE_5__.runningVdkOperation !== 'jp-vdk:menu-convert-job-to-notebook') {
                (0,_initVDKConfigCell__WEBPACK_IMPORTED_MODULE_6__.initVDKConfigCell)(notebookTracker);
            }
            else {
                //  * Populates notebook with provided content for convert job operation
                //  * Check src/components/ConvertJobToNotebook.tsx for more
                (0,_components_ConvertJobToNotebook__WEBPACK_IMPORTED_MODULE_7__.populateNotebook)(notebookTracker);
            }
        });
        (0,_components_StatusButton__WEBPACK_IMPORTED_MODULE_8__.createStatusMenu)(commands);
        const statusButton = (0,_components_StatusButton__WEBPACK_IMPORTED_MODULE_8__.createStatusButton)(commands);
        const fileBrowser = factory.defaultBrowser;
        app.restored.then(() => {
            const topPanel = document.querySelector('#jp-top-panel');
            if (topPanel) {
                topPanel.appendChild(statusButton.element);
            }
        });
        (0,_commandsAndMenu__WEBPACK_IMPORTED_MODULE_5__.updateVDKMenu)(commands, docManager, fileBrowser, notebookTracker, statusButton);
        fileBrowser.model.pathChanged.connect(onPathChanged);
        (0,_vdkTags__WEBPACK_IMPORTED_MODULE_9__.trackVdkTags)(notebookTracker, themeManager);
        await (0,_tokenUpdate__WEBPACK_IMPORTED_MODULE_10__.setupTokenCheckInterval)();
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);
const onPathChanged = async (model, change) => {
    workingDirectory = change.newValue;
};


/***/ }),

/***/ "./lib/initVDKConfigCell.js":
/*!**********************************!*\
  !*** ./lib/initVDKConfigCell.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   initVDKConfigCell: () => (/* binding */ initVDKConfigCell)
/* harmony export */ });
/*
 * Copyright 2021-2023 VMware, Inc.
 * SPDX-License-Identifier: Apache-2.0
 */
/**
 * This func adds a cell with the necessary commands to enable VDK for a Jupyter notebook
 */
function initVDKConfigCell(notebookTracker) {
    var _a, _b, _c, _d;
    const notebookPanel = notebookTracker.currentWidget;
    if (notebookPanel) {
        const initCell = (_b = (_a = notebookPanel.content.model) === null || _a === void 0 ? void 0 : _a.contentFactory) === null || _b === void 0 ? void 0 : _b.createCodeCell({
            cell: {
                cell_type: 'code',
                source: [
                    `"""\n`,
                    `vdk.plugin.ipython extension introduces a magic command for Jupyter.\n`,
                    `The command enables the user to load VDK for the current notebook.\n`,
                    `VDK provides the job_input API, which has methods for:\n`,
                    `    * executing queries to an OLAP database;\n`,
                    `    * ingesting data into a database;\n`,
                    `    * processing data into a database.\n`,
                    `See the IJobInput documentation for more details.\n`,
                    `https://github.com/vmware/versatile-data-kit/blob/main/projects/vdk-core/src/vdk/api/job_input.py\n`,
                    `Please refrain from tagging this cell with VDK as it is not an actual part of the data job\n`,
                    `and is only used for development purposes.\n`,
                    `"""\n`,
                    `%reload_ext vdk.plugin.ipython\n`,
                    `%reload_VDK\n`,
                    `job_input = VDK.get_initialized_job_input()`
                ],
                metadata: {}
            }
        });
        const cells = (_d = (_c = notebookTracker.currentWidget) === null || _c === void 0 ? void 0 : _c.content.model) === null || _d === void 0 ? void 0 : _d.cells;
        const cellContent = cells === null || cells === void 0 ? void 0 : cells.get(0).value.text;
        // check if the notebook has only 1 empty cell, which is how we judge if it is a new notebook or not
        if (cells && initCell && cells.length <= 1 && cellContent == '') {
            cells.insert(0, initCell);
            cells.remove(1);
        }
    }
}


/***/ }),

/***/ "./lib/jobData.js":
/*!************************!*\
  !*** ./lib/jobData.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   checkIfVdkOptionDataIsDefined: () => (/* binding */ checkIfVdkOptionDataIsDefined),
/* harmony export */   getJobDataJsonObject: () => (/* binding */ getJobDataJsonObject),
/* harmony export */   jobData: () => (/* binding */ jobData),
/* harmony export */   setJobDataToDefault: () => (/* binding */ setJobDataToDefault)
/* harmony export */ });
/* harmony import */ var _vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./vdkOptions/vdk_options */ "./lib/vdkOptions/vdk_options.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/*
 * Copyright 2023-2023 VMware, Inc.
 * SPDX-License-Identifier: Apache-2.0
 */
/*
 * This enum is automatically generated from the enum from  ../vdk-jupyterlab-extension/vdk_options/vdk_options_.py
 * Using https://github.com/Syndallic/py-to-ts-interfaces#example
 * The enum shall not be modified directly
 */


/*
 * A global variable which holds the information about the current job.
 * This variable acts like session storage that holds information about the data job for the currently running Jupyter instance
 * The values of its properties are meant to be changed during a VDK operation and after the operation ends they need to be set to default.
 */
var jobData = new Map([]);
/*
 * Function responsible for reverting all vdkOption values of jobData to default
 */
function setJobDataToDefault() {
    for (const option of Object.values(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_1__.VdkOption)) {
        jobData.set(option, '');
    }
}
/*
 * Sets default VdkOption values to jobData when the extension is firstly loaded
 */
setJobDataToDefault();
/*
 * Function that return the JSON object of jobData
 * TODO: find a better wat to parse the Map into JSON object
 */
function getJobDataJsonObject() {
    const jsObj = {
        jobName: jobData.get(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_1__.VdkOption.NAME),
        jobTeam: jobData.get(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_1__.VdkOption.TEAM),
        jobPath: jobData.get(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_1__.VdkOption.PATH),
        jobArguments: jobData.get(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_1__.VdkOption.ARGUMENTS),
        deploymentReason: jobData.get(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_1__.VdkOption.DEPLOYMENT_REASON)
    };
    return jsObj;
}
/*
 * Function that checks whether a value is defined in jobData
 * Shows dialog that operation cannot be performed because of undefined value
 */
async function checkIfVdkOptionDataIsDefined(option) {
    if (jobData.get(option))
        return true;
    else {
        await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)('Encountered an error while trying to execute operation. Error:', 'The ' + option + ' should be defined!', [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton()]);
        return false;
    }
}


/***/ }),

/***/ "./lib/serverRequests.js":
/*!*******************************!*\
  !*** ./lib/serverRequests.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   getNotebookInfo: () => (/* binding */ getNotebookInfo),
/* harmony export */   getServerDirRequest: () => (/* binding */ getServerDirRequest),
/* harmony export */   getVdkCellIndices: () => (/* binding */ getVdkCellIndices),
/* harmony export */   jobConvertToNotebookRequest: () => (/* binding */ jobConvertToNotebookRequest),
/* harmony export */   jobRequest: () => (/* binding */ jobRequest),
/* harmony export */   jobRunRequest: () => (/* binding */ jobRunRequest),
/* harmony export */   jobdDataRequest: () => (/* binding */ jobdDataRequest)
/* harmony export */ });
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jobData__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./jobData */ "./lib/jobData.js");
/* harmony import */ var _vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./vdkOptions/vdk_options */ "./lib/vdkOptions/vdk_options.js");
/*
 * Copyright 2021-2023 VMware, Inc.
 * SPDX-License-Identifier: Apache-2.0
 */




const showError = async (error) => {
    await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)('Encountered an error while trying to connect the server. Error:', error, [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton()]);
};
/**
 * Sent a POST request to the server to run a data job.
 * The information about the data job is retrieved from jobData object and sent as JSON.
 * Returns a pair of boolean (representing whether the vdk run was run) and a string (representing the result of vdk run)
 */
async function jobRunRequest() {
    if (await (0,_jobData__WEBPACK_IMPORTED_MODULE_1__.checkIfVdkOptionDataIsDefined)(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_2__.VdkOption.PATH)) {
        try {
            const data = await (0,_handler__WEBPACK_IMPORTED_MODULE_3__.requestAPI)('run', {
                body: JSON.stringify((0,_jobData__WEBPACK_IMPORTED_MODULE_1__.getJobDataJsonObject)()),
                method: 'POST'
            });
            return { message: data['message'], status: data['message'] == '0' };
        }
        catch (error) {
            showError(error);
            return { message: '', status: false };
        }
    }
    else {
        return { message: '', status: false };
    }
}
/**
 * Sent a POST request to the server to execute a VDK operation a data job.
 * The information about the data job is retrieved from jobData object and sent as JSON.
 */
async function jobRequest(endPoint) {
    if ((await (0,_jobData__WEBPACK_IMPORTED_MODULE_1__.checkIfVdkOptionDataIsDefined)(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_2__.VdkOption.NAME)) &&
        (await (0,_jobData__WEBPACK_IMPORTED_MODULE_1__.checkIfVdkOptionDataIsDefined)(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_2__.VdkOption.TEAM))) {
        try {
            const data = await (0,_handler__WEBPACK_IMPORTED_MODULE_3__.requestAPI)(endPoint, {
                body: JSON.stringify((0,_jobData__WEBPACK_IMPORTED_MODULE_1__.getJobDataJsonObject)()),
                method: 'POST'
            });
            if (!data['error'])
                alert(data['message']);
            else {
                await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)('Encountered an error while trying the ' +
                    endPoint +
                    ' operation. Error:', data['message'], [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton()]);
            }
        }
        catch (error) {
            showError(error);
        }
    }
}
/**
 * Sends a POST request to the server to perform a 'transform job to notebook' operation.
 * This function prepares the job data and makes the request.
 *
 * Upon success, the server returns an object containing:
 * - message: A string that includes the 'codeStructure' and 'filenames' os the steps of the transformed job.
 * - status: A boolean indicating the operation's success. It's '' when no errors occurred during the operation.
 *
 * Upon failure (either server-side or client-side), the function returns an object
 * with an error message and 'false' status.
 * Any error that occurred during the operation is also shown to the user.
 *
 * @returns A Promise that resolves to an object containing the message from the server and the status of the operation.
 */
async function jobConvertToNotebookRequest() {
    if (await (0,_jobData__WEBPACK_IMPORTED_MODULE_1__.checkIfVdkOptionDataIsDefined)(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_2__.VdkOption.PATH)) {
        try {
            const data = await (0,_handler__WEBPACK_IMPORTED_MODULE_3__.requestAPI)('convertJobToNotebook', {
                body: JSON.stringify((0,_jobData__WEBPACK_IMPORTED_MODULE_1__.getJobDataJsonObject)()),
                method: 'POST'
            });
            return { message: data['message'], status: data['error'] == '' };
        }
        catch (error) {
            showError(error);
            return { message: '', status: false };
        }
    }
    else {
        return {
            message: 'The job path is not defined. Please define it before attempting to convert the job to a notebook.',
            status: false
        };
    }
}
/**
 * Sent a POST request to the server to get information about the data job of current directory
 */
async function jobdDataRequest() {
    try {
        const data = await (0,_handler__WEBPACK_IMPORTED_MODULE_3__.requestAPI)('job', {
            body: JSON.stringify(JSON.stringify((0,_jobData__WEBPACK_IMPORTED_MODULE_1__.getJobDataJsonObject)())),
            method: 'POST'
        });
        if (data) {
            _jobData__WEBPACK_IMPORTED_MODULE_1__.jobData.set(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_2__.VdkOption.NAME, data[_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_2__.VdkOption.NAME]);
            _jobData__WEBPACK_IMPORTED_MODULE_1__.jobData.set(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_2__.VdkOption.TEAM, data[_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_2__.VdkOption.TEAM]);
            _jobData__WEBPACK_IMPORTED_MODULE_1__.jobData.set(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_2__.VdkOption.PATH, data[_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_2__.VdkOption.PATH]);
        }
    }
    catch (error) {
        showError(error);
    }
}
/**
 * Sent a POST request to the server to get more information about the notebook that includes a cell with the given id
 * Returns the path to the notebook file and the index of the cell with the spicific id
 * If no such notebook in the current directory or no notebook with a cell with such an id is found return empty strings
 */
async function getNotebookInfo(cellId) {
    const dataToSend = {
        cellId: cellId,
        jobPath: _jobData__WEBPACK_IMPORTED_MODULE_1__.jobData.get(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_2__.VdkOption.PATH)
    };
    if (await (0,_jobData__WEBPACK_IMPORTED_MODULE_1__.checkIfVdkOptionDataIsDefined)(_vdkOptions_vdk_options__WEBPACK_IMPORTED_MODULE_2__.VdkOption.PATH)) {
        try {
            const data = await (0,_handler__WEBPACK_IMPORTED_MODULE_3__.requestAPI)('notebook', {
                body: JSON.stringify(dataToSend),
                method: 'POST'
            });
            return {
                path: data['path'],
                cellIndex: data['cellIndex']
            };
        }
        catch (error) {
            return {
                path: '',
                cellIndex: ''
            };
        }
    }
    else {
        return {
            path: '',
            cellIndex: ''
        };
    }
}
/**
 * Sent a POST request to the server to indices of the vdk cells of a notebook
 * Returns an Array with indices if vdk cells are found and empty array if not
 */
async function getVdkCellIndices(nbPath) {
    try {
        const dataToSend = {
            nbPath: nbPath
        };
        const data = await (0,_handler__WEBPACK_IMPORTED_MODULE_3__.requestAPI)('vdkCellIndices', {
            body: JSON.stringify(dataToSend),
            method: 'POST'
        });
        return data;
    }
    catch (error) {
        showError(error);
    }
    return [];
}
async function getServerDirRequest() {
    const data = await (0,_handler__WEBPACK_IMPORTED_MODULE_3__.requestAPI)('serverPath', {
        method: 'GET'
    });
    if (data) {
        return data;
    }
    else {
        await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)("Encountered an error while trying to connect the server. Error: \
      the server's location cannot be identified!", [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton()]);
        return '';
    }
}


/***/ }),

/***/ "./lib/tokenUpdate.js":
/*!****************************!*\
  !*** ./lib/tokenUpdate.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   fetchTokenLocation: () => (/* binding */ fetchTokenLocation),
/* harmony export */   getTokenFromLocation: () => (/* binding */ getTokenFromLocation),
/* harmony export */   sendTokenToServer: () => (/* binding */ sendTokenToServer),
/* harmony export */   setupTokenCheckInterval: () => (/* binding */ setupTokenCheckInterval)
/* harmony export */ });
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");

async function fetchTokenLocation() {
    const data = await (0,_handler__WEBPACK_IMPORTED_MODULE_0__.requestAPI)('vdkAccessTokenLocation', {
        method: 'GET'
    });
    if (data) {
        return data || '';
    }
    else {
        console.error("Couldn't fetch token location from the server");
        return '';
    }
}
function safeJSONParse(value) {
    try {
        return JSON.parse(value || 'null');
    }
    catch (_a) {
        return null;
    }
}
async function getTokenFromLocation(location) {
    const parts = location.split(':');
    const storageType = parts[0];
    const path = parts[1].split('.');
    if (storageType === "localStorage") {
        let item = safeJSONParse(window.top.localStorage.getItem(path[0]));
        return path.reduce((current, key) => {
            return current && key in current ? current[key] : null;
        }, item);
    }
    return null;
}
async function sendTokenToServer(token) {
    try {
        await (0,_handler__WEBPACK_IMPORTED_MODULE_0__.requestAPI)('vdkAccessToken', {
            body: JSON.stringify({ token }),
            method: 'POST'
        });
    }
    catch (error) {
        console.error("Couldn't send token to server", error);
    }
}
const CHECK_INTERVAL_MS = 60000;
/**
 * Checks for the presence of a token and sends it to the server if found.
 *
 * This function fetches the token location, retrieves the token from the specified location,
 * and sends the token to the server.
 *
 * @returns {Promise<string>} - Returns the token location. If the token is not found then we should not schedule regular update.
 */
async function checkToken() {
    const tokenLocation = await fetchTokenLocation();
    console.debug("Checking token location");
    if (tokenLocation) {
        const token = await getTokenFromLocation(tokenLocation);
        if (token) {
            await sendTokenToServer(token);
        }
    }
    return tokenLocation;
}
/**
 * Setups regularly to update the access token from the parent
 */
async function setupTokenCheckInterval() {
    const initialTokenLocation = await checkToken(); // Run immediately
    if (initialTokenLocation) {
        console.log("Initial token location is " + initialTokenLocation);
        console.log("Schedule regular update every " + CHECK_INTERVAL_MS);
        setInterval(checkToken, CHECK_INTERVAL_MS);
    }
    else {
        console.log("No token location. Disable regular token update");
    }
}


/***/ }),

/***/ "./lib/utils.js":
/*!**********************!*\
  !*** ./lib/utils.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   CONVERT_JOB_TO_NOTEBOOK_BUTTON_LABEL: () => (/* binding */ CONVERT_JOB_TO_NOTEBOOK_BUTTON_LABEL),
/* harmony export */   CREATE_DEP_BUTTON_LABEL: () => (/* binding */ CREATE_DEP_BUTTON_LABEL),
/* harmony export */   CREATE_JOB_BUTTON_LABEL: () => (/* binding */ CREATE_JOB_BUTTON_LABEL),
/* harmony export */   DELETE_JOB_BUTTON_LABEL: () => (/* binding */ DELETE_JOB_BUTTON_LABEL),
/* harmony export */   DOWNLOAD_JOB_BUTTON_LABEL: () => (/* binding */ DOWNLOAD_JOB_BUTTON_LABEL),
/* harmony export */   RUN_FAILED_BUTTON_LABEL: () => (/* binding */ RUN_FAILED_BUTTON_LABEL),
/* harmony export */   RUN_JOB_BUTTON_LABEL: () => (/* binding */ RUN_JOB_BUTTON_LABEL),
/* harmony export */   STATUS_BUTTON_CLASS: () => (/* binding */ STATUS_BUTTON_CLASS),
/* harmony export */   STATUS_BUTTON_COMMAND_ID: () => (/* binding */ STATUS_BUTTON_COMMAND_ID),
/* harmony export */   STATUS_BUTTON_ID: () => (/* binding */ STATUS_BUTTON_ID),
/* harmony export */   STATUS_BUTTON_LABEL: () => (/* binding */ STATUS_BUTTON_LABEL)
/* harmony export */ });
/*
 * Copyright 2021-2023 VMware, Inc.
 * SPDX-License-Identifier: Apache-2.0
 */
const CONVERT_JOB_TO_NOTEBOOK_BUTTON_LABEL = 'Convert Job To Notebook';
const RUN_JOB_BUTTON_LABEL = 'Run Job';
const CREATE_DEP_BUTTON_LABEL = 'Create Deployment';
const CREATE_JOB_BUTTON_LABEL = 'Create Job';
const RUN_FAILED_BUTTON_LABEL = 'Run Failed';
const DOWNLOAD_JOB_BUTTON_LABEL = 'Download Job';
const DELETE_JOB_BUTTON_LABEL = 'Delete Job';
const STATUS_BUTTON_LABEL = 'Status';
const STATUS_BUTTON_CLASS = 'jp-vdk-check-status-button';
const STATUS_BUTTON_COMMAND_ID = 'jp-vdk:check-status-button';
const STATUS_BUTTON_ID = 'jp-vdk-check-status-button';


/***/ }),

/***/ "./lib/vdkOptions/vdk_options.js":
/*!***************************************!*\
  !*** ./lib/vdkOptions/vdk_options.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   VdkOption: () => (/* binding */ VdkOption)
/* harmony export */ });
/*
 * Copyright 2023-2023 VMware, Inc.
 * SPDX-License-Identifier: Apache-2.0
 */
var VdkOption;
(function (VdkOption) {
    VdkOption["NAME"] = "jobName";
    VdkOption["TEAM"] = "jobTeam";
    VdkOption["PATH"] = "jobPath";
    VdkOption["ARGUMENTS"] = "jobArguments";
    VdkOption["DEPLOYMENT_REASON"] = "deploymentReason";
})(VdkOption || (VdkOption = {}));


/***/ }),

/***/ "./lib/vdkTags.js":
/*!************************!*\
  !*** ./lib/vdkTags.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   addNumberElement: () => (/* binding */ addNumberElement),
/* harmony export */   addVdkCellDesign: () => (/* binding */ addVdkCellDesign),
/* harmony export */   addVdkLogo: () => (/* binding */ addVdkLogo),
/* harmony export */   trackVdkTags: () => (/* binding */ trackVdkTags)
/* harmony export */ });
/* harmony import */ var _serverRequests__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./serverRequests */ "./lib/serverRequests.js");
/*
 * Copyright 2021-2023 VMware, Inc.
 * SPDX-License-Identifier: Apache-2.0
 */

const addNumberElement = (number, node) => {
    const numberElement = document.createElement('div');
    numberElement.innerText = String(number);
    node.classList.contains('jp-vdk-failing-cell')
        ? numberElement.classList.add('jp-vdk-failing-cell-num')
        : numberElement.classList.add('jp-vdk-cell-num');
    node.appendChild(numberElement);
};
const addVdkLogo = (node) => {
    const logo = document.createElement('img');
    logo.setAttribute('src', 'https://raw.githubusercontent.com/vmware/versatile-data-kit/dc15f7489f763a0e0e29370b2e06a714448fc234/support/images/versatile-data-kit-logo.svg');
    logo.setAttribute('width', '20');
    logo.setAttribute('height', '20');
    logo.classList.add('jp-vdk-logo');
    node.appendChild(logo);
};
const addVdkCellDesign = (cells, vdkCellIndices, themeManager, currentCell) => {
    // Delete previous numbering in case of untagging elements
    const vdkCellNums = Array.from(document.getElementsByClassName('jp-vdk-cell-num'));
    vdkCellNums.forEach(element => {
        element.remove();
    });
    // Delete previous fail numbering
    const vdkFailingCellNums = Array.from(document.getElementsByClassName('jp-vdk-failing-cell-num'));
    vdkFailingCellNums.forEach(element => {
        element.remove();
    });
    // Delete previously added logo in case of untagging elements
    const vdkCellLogo = Array.from(document.getElementsByClassName('jp-vdk-logo'));
    vdkCellLogo.forEach(element => {
        element.remove();
    });
    let vdkCellCounter = 0;
    for (let i = 0; i < cells.length; i++) {
        if (vdkCellIndices.includes(i)) {
            if (themeManager.theme &&
                themeManager.isLight(themeManager.theme.toString())) {
                cells[i].classList.remove('jp-vdk-cell-dark');
                cells[i].classList.add('jp-vdk-cell');
            }
            else {
                cells[i].classList.add('jp-vdk-cell');
                cells[i].classList.add('jp-vdk-cell-dark');
            }
            // We do not add logo to the active cell since it blocks other UI elements
            if (currentCell && cells[i] != currentCell) {
                addVdkLogo(cells[i]);
            }
            addNumberElement(++vdkCellCounter, cells[i]);
        }
        else {
            cells[i].classList.remove('jp-vdk-cell');
            cells[i].classList.remove('jp-vdk-cell-dark');
        }
    }
};
const trackVdkTags = (notebookTracker, themeManager) => {
    const changeCells = async () => {
        if (notebookTracker.currentWidget &&
            notebookTracker.currentWidget.model &&
            notebookTracker.currentWidget.model.cells.length !== 0) {
            // Get indices of the vdk cells using cell metadata
            let vdkCellIndices = [];
            let cellIndex = 0;
            while (notebookTracker.currentWidget &&
                notebookTracker.currentWidget.model &&
                notebookTracker.currentWidget.model.cells.get(cellIndex)) {
                const currentCellTags = notebookTracker.currentWidget.model.cells
                    .get(cellIndex)
                    .metadata.get('tags');
                if (currentCellTags && currentCellTags.includes('vdk'))
                    vdkCellIndices.push(cellIndex);
                cellIndex++;
            }
            // this case covers the use case when the notebook is loaded for the first time
            if (!vdkCellIndices.length) {
                vdkCellIndices = await (0,_serverRequests__WEBPACK_IMPORTED_MODULE_0__.getVdkCellIndices)(notebookTracker.currentWidget.context.path);
            }
            if (vdkCellIndices.length > 0 &&
                notebookTracker.activeCell &&
                notebookTracker.activeCell.parent &&
                notebookTracker.activeCell.parent.node.children) {
                addVdkCellDesign(Array.from(notebookTracker.activeCell.parent.node.children), vdkCellIndices, themeManager, notebookTracker.activeCell.node);
            }
        }
    };
    notebookTracker.activeCellChanged.connect(changeCells);
    themeManager.themeChanged.connect(changeCells);
};


/***/ })

}]);
//# sourceMappingURL=lib_commandsAndMenu_js-lib_index_js.570180ee2c5d2be18376.js.map