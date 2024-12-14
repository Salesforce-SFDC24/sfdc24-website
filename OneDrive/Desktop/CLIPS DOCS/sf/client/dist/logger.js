/*
 * Copyright (c) 2023, salesforce.com, inc.
 * All rights reserved.
 * Licensed under the BSD 3-Clause license.
 * For full license text, see LICENSE.txt file in the repo root or https://opensource.org/licenses/BSD-3-Clause
 */
import { format } from 'node:util';
import { Logger } from '@salesforce/core/logger';
const customLogger = (namespace) => {
    const sfLogger = new Logger(namespace);
    return {
        child: (ns, delimiter) => customLogger(`${namespace}${delimiter ?? ':'}${ns}`),
        debug: (formatter, ...args) => sfLogger.debug(format(formatter, ...args)),
        error: (formatter, ...args) => sfLogger.error(format(formatter, ...args)),
        info: (formatter, ...args) => sfLogger.info(format(formatter, ...args)),
        trace: (formatter, ...args) => sfLogger.trace(format(formatter, ...args)),
        warn: (formatter, ...args) => sfLogger.warn(format(formatter, ...args)),
        namespace,
    };
};
export const logger = customLogger('sf:oclif');
export const sfStartupLogger = customLogger('sf-startup');
//# sourceMappingURL=logger.js.map