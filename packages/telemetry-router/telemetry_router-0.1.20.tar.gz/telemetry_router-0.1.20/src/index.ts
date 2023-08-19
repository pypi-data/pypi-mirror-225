import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { NotebookPanel } from '@jupyterlab/notebook';

import { INotebookContent } from '@jupyterlab/nbformat';

import { Token } from '@lumino/coreutils';

import { requestAPI } from './handler';

const PLUGIN_ID = 'telemetry-router:plugin';

export const ITelemetryRouter = new Token<ITelemetryRouter>(PLUGIN_ID);

export interface ITelemetryRouter {
  loadNotebookPanel(notebookPanel: NotebookPanel): void;
  publishEvent(eventDetail: Object, logNotebookContent?: Boolean): void;
}

class TelemetryRouter implements ITelemetryRouter {
  private sessionID?: string;
  private notebookPanel?: NotebookPanel;

  /**
   * Load notebookPanel.
   *
   * @param {NotebookPanel} notebookPanel
   */
  async loadNotebookPanel(notebookPanel: NotebookPanel) {
    this.notebookPanel = notebookPanel;
  }

  /**
   * Send event data to exporters defined in the configuration file.
   *
   * @param {Object} eventDetail An object containing event details
   * @param {Boolean} logNotebookContent A boolean indicating whether to log the entire notebook or not
   */
  async publishEvent(eventDetail: Object, logNotebookContent?: Boolean) {
    if (!this.notebookPanel) {
      throw Error('router needs to load notebookPanel first.');
    }

    // Check if session id received is equal to the stored session id
    if (
      !this.sessionID ||
      this.sessionID !== this.notebookPanel?.sessionContext.session?.id
    ) {
      this.sessionID = this.notebookPanel?.sessionContext.session?.id;
    }

    // Construct data
    const requestBody = {
      eventDetail: eventDetail,
      notebookState: {
        sessionID: this.sessionID,
        notebookPath: this.notebookPanel?.context.path,
        notebookContent: logNotebookContent
          ? (this.notebookPanel?.model?.toJSON() as INotebookContent)
          : null // decide whether to log the entire notebook
      }
    };

    // Send data to exporters
    const response = await requestAPI<any>('export', {
      method: 'POST',
      body: JSON.stringify(requestBody)
    });
    console.log(response);
  }
}

/**
 * Activate the extension
 *
 * @param {JupyterFrontEnd} app - The JupyterLab application instance.
 * @return {Promise<TelemetryRouter>} - A promise that returns TelemetryRouter if resolved.
 */
async function activate(app: JupyterFrontEnd): Promise<TelemetryRouter> {
  const version = await requestAPI<string>('version');
  console.log(`${PLUGIN_ID}: ${version}`);
  const telemetryRouter = new TelemetryRouter();
  return telemetryRouter;
}

const plugin: JupyterFrontEndPlugin<TelemetryRouter> = {
  id: PLUGIN_ID,
  provides: ITelemetryRouter,
  autoStart: true,
  activate: activate
};

export default plugin;
