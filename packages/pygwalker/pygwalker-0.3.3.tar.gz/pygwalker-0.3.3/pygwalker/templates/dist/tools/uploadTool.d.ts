import React from 'react';
import type { IAppProps } from '../interfaces';
import type { ToolbarButtonItem } from "@kanaries/graphic-walker/dist/components/toolbar/toolbar-button";
import type { IGlobalStore } from '@kanaries/graphic-walker/dist/store';
export declare function getUploadTool(props: IAppProps, storeRef: React.MutableRefObject<IGlobalStore | null>): ToolbarButtonItem;
