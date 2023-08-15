import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
} from '@jupyterlab/application';

import { NotebookPanel } from '@jupyterlab/notebook';

import { INotebookContent } from '@jupyterlab/nbformat';

import { Token } from '@lumino/coreutils';

import {
  trace,
  context,
  SpanStatusCode
} from "@opentelemetry/api";

// import {
//   // Consumer,
//   // ConsoleLogger,
//   // MongoDBLogger,
//   // S3Logger,
//   // InfluxDBLogger,
//   ConsumerCollection,
// } from './consumer';

import { requestAPI } from './handler';

import { registerTracerProvider } from './otel';

registerTracerProvider();
const tracer = trace.getTracer('telemetry'); // Returns a tracer from the **global** tracer provider.

let rootSpan: any;
const spanContextInjector = (data: any) => {
  if (data.eventDetail.eventName) {
    if (!rootSpan) {
      rootSpan = tracer.startSpan(data.eventDetail.eventName)
      rootSpan.setAttribute('event', JSON.stringify(data))
      rootSpan.setStatus({
        code: SpanStatusCode.OK,
        message: 'OK'
      })
      rootSpan.end()
    }
    else {
      const ctx = trace.setSpan(context.active(), rootSpan);
      const span = tracer.startSpan(data.eventDetail.eventName, undefined, ctx)
      span.setAttribute('event', JSON.stringify(data))
      span.setStatus({
        code: SpanStatusCode.OK,
        message: 'OK'
      })
      span.end()
    }
  }
}

const PLUGIN_ID = 'telemetry-router:plugin';

export const ITelemetryRouter = new Token<ITelemetryRouter>(PLUGIN_ID)

export interface ITelemetryRouter {
  loadNotebookPanel(notebookPanel: NotebookPanel): void;
  publishEvent(eventDetail: Object, logNotebookContent?: Boolean): void;
}

export class TelemetryRouter implements ITelemetryRouter {
  // private sessionID?: string;
  // private sequence: number = 0;
  private notebookPanel?: NotebookPanel;

  loadNotebookPanel(notebookPanel: NotebookPanel) {
    this.notebookPanel = notebookPanel
  }

  async publishEvent(eventDetail: Object, logNotebookContent?: Boolean) {
    // // Check if session id received is equal to the stored session id &
    // // Update sequence number accordingly
    // if (this.sessionID && this.sessionID === this.notebookPanel?.sessionContext.session?.id) {
    //   this.sequence = this.sequence + 1
    // }
    // else {
    //   this.sessionID = this.notebookPanel?.sessionContext.session?.id
    //   this.sequence = 0
    // }

    // Get environment data
    const { workspaceID } = await requestAPI<any>('env')

    // Construct data
    const data = {
      eventDetail: eventDetail,
      notebookState: {
        // sessionID: this.sessionID,
        // sequence: this.sequence,
        workspaceID: workspaceID,
        notebookPath: this.notebookPanel?.context.path,
        notebookContent: logNotebookContent ? this.notebookPanel?.model?.toJSON() as INotebookContent : null
      },
    }

    spanContextInjector(data)

    // // Send to consumer
    // ConsumerCollection.forEach(consumer => {
    //   if (consumer.id == 'ConsoleLogger') {
    //     new consumer().consume(log);
    //   }
    // });
  }
}

const plugin: JupyterFrontEndPlugin<TelemetryRouter> = {
  id: PLUGIN_ID,
  description: 'A JupyterLab extension.',
  provides: ITelemetryRouter,
  autoStart: true,
  activate: async (app: JupyterFrontEnd) => {
    const version = await requestAPI<string>('version')
    console.log(`${PLUGIN_ID}: ${version}`)

    const telemetryRouter = new TelemetryRouter();

    return telemetryRouter;
  }
};

export default plugin;
