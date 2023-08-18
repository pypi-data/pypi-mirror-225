import { ReactElement } from "react";
export interface INotification {
    title: string;
    message: string | ReactElement;
    type: "success" | "error" | "info" | "warning";
}
export declare function useNotification(): {
    notify: (not: INotification, t: number) => void;
};
declare const NotificationWrapper: React.FC<{
    children: ReactElement;
}>;
export default NotificationWrapper;
