import type { IDataSourceProps } from "../interfaces";
import type { IRow, IDataQueryPayload } from "@kanaries/graphic-walker/dist/interfaces";
declare global {
    export interface Window {
        dslToSql: (datasetStr: string, PayloadStr: string) => string;
    }
}
interface ICommPostDataMessage {
    dataSourceId: string;
    data?: IRow[];
    total: number;
    curIndex: number;
}
export declare function loadDataSource(props: IDataSourceProps): Promise<IRow[]>;
export declare function postDataService(msg: ICommPostDataMessage): void;
export declare function finishDataService(msg: any): void;
export declare function getDatasFromKernel(payload: IDataQueryPayload): Promise<IRow[]>;
export {};
