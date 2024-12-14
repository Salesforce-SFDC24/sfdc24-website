/*
 * Copyright (c) 2022, salesforce.com, inc.
 * All rights reserved.
 * Licensed under the BSD 3-Clause license.
 * For full license text, see LICENSE.txt file in the repo root or https://opensource.org/licenses/BSD-3-Clause
 */
import { CommandHelp } from '@oclif/core/help';
export class SfCommandHelp extends CommandHelp {
    constructor(command, config, opts) {
        super(command, config, opts);
        this.command = command;
        this.config = config;
        this.opts = opts;
        this.shortHelp = false;
    }
    get showShortHelp() {
        return this.shortHelp;
    }
    set showShortHelp(shortHelp) {
        this.shortHelp = shortHelp;
    }
    sections() {
        const sections = super.sections();
        if (this.shortHelp) {
            return sections.filter(({ header }) => ['USAGE', 'ARGUMENTS', 'FLAGS'].includes(header));
        }
        const additionalSfSections = [
            {
                header: 'CONFIGURATION VARIABLES',
                generate: ({ cmd }) => cmd.configurationVariablesSection,
            },
            {
                header: 'ENVIRONMENT VARIABLES',
                generate: ({ cmd }) => cmd.envVariablesSection,
            },
            {
                header: 'ERROR CODES',
                generate: ({ cmd }) => cmd.errorCodes,
            },
        ];
        const flagsIndex = (sections.findIndex((section) => section.header === 'FLAG DESCRIPTIONS') || sections.length - 1) + 1;
        sections.splice(flagsIndex, 0, additionalSfSections[0]);
        sections.splice(flagsIndex + 1, 0, additionalSfSections[1]);
        sections.splice(flagsIndex + 2, 0, additionalSfSections[2]);
        return sections;
    }
}
//# sourceMappingURL=sfCommandHelp.js.map