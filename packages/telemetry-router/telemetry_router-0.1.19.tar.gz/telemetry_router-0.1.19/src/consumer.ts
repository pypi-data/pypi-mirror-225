import { requestAPI } from "./handler";

abstract class BaseLogger {
    static id = 'BaseLogger';
    abstract consume(log: any): void;
}

export class ConsoleLogger extends BaseLogger {
    static id = 'ConsoleLogger';
    consume(log: any) {
        console.log('ConsoleLogger', log);
    }
}

export class MongoDBLogger extends BaseLogger {
    static id = 'MongoDBLogger'
    async consume(log: any) {
        const responseMongo = await requestAPI<any>('mongo', { method: 'POST', body: JSON.stringify(log) });
        const data = {
            request: log,
            response: responseMongo
        }
        console.log('MongoDBLogger', data);
    }
}

export class S3Logger extends BaseLogger {
    static id = 'S3Logger'
    async consume(log: any) {
        const responseS3 = await requestAPI<any>('s3', { method: 'POST', body: JSON.stringify(log) });
        const data = {
            request: log,
            response: responseS3
        }
        console.log('S3Logger', data);
    }
}

// export class InfluxDBLogger extends Consumer {
//     constructor() { super() }
//     async consume(log: any) {
//         const responseInflux = await requestAPI<any>('influx', { method: 'POST', body: JSON.stringify(log) });
//         const data = {
//             request: log,
//             response: responseInflux
//         }
//         console.log('InfluxDBLogger', data);
//     }
// }

export const ConsumerCollection = [
    ConsoleLogger,
    MongoDBLogger,
    S3Logger
]