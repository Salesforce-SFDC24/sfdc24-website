/*
 * Copyright (c) 2022, salesforce.com, inc.
 * All rights reserved.
 * Licensed under the BSD 3-Clause license.
 * For full license text, see LICENSE.txt file in the repo root or https://opensource.org/licenses/BSD-3-Clause
 */
import { Help } from '@oclif/core/help';
import { toConfiguredId } from '@oclif/core/util/ids';
import { Ansis } from 'ansis';
import { colorize } from '@oclif/core/ux';
import { SfCommandHelp } from './sfCommandHelp.js';
const ansis = new Ansis();
export default class SfHelp extends Help {
    constructor(config, opts) {
        super(config, opts);
        this.CommandHelpClass = SfCommandHelp;
        this.showShortHelp = false;
        this.commands = [];
        this.commands = this.config.commandIDs.map((c) => `${this.config.bin} ${toConfiguredId(c, this.config)}`);
        const regexes = [];
        for (const cmd of this.commands) {
            const subCommands = this.commands.filter((c) => c !== cmd && c.startsWith(cmd)).map((c) => c.replace(cmd, ''));
            /**
             * This regex matches any command in the help output.
             * It will continue to match until the next space, quote, or period.
             *
             * Examples that will match (see sf project deploy start as an example):
             * - sf deploy project start
             * - "sf deploy project start"
             * - sf org create scratch|sandbox
             * - "sf org create scratch|sandbox"
             *
             * It will not match any child commands of the current command.
             * For instance, the examples in `sf org list metadata --help` should match `sf org list metadata` but not `sf org list`.
             *
             * Example of constructed regex that won't match child commands:
             * - /sf org list([^\s".]+)?(?! auth| limits| sobject record-counts| metadata| metadata-types| users)/g
             * - /sf org list metadata([^\s".]+)?(?!-types)/g
             */
            let regexString = `${cmd}([^\\s".]+)?`;
            if (subCommands.length)
                regexString += `(?!${subCommands.join('|')})`;
            regexes.push(regexString);
        }
        this.commandIdRegex = new RegExp(regexes.join('|'), 'g');
    }
    async showHelp(argv) {
        this.showShortHelp = argv.includes('-h');
        return super.showHelp(argv);
    }
    getCommandHelpClass(command) {
        this.commandHelpClass = super.getCommandHelpClass(command);
        this.commandHelpClass.showShortHelp = this.showShortHelp;
        return this.commandHelpClass;
    }
    log(...args) {
        const formatted = args.map((arg) => {
            let formattedArg = arg.slice();
            const matches = ansis.strip(formattedArg).match(this.commandIdRegex) ?? [];
            for (const match of matches) {
                formattedArg = formattedArg.replaceAll(match, colorize('dim', match));
            }
            return formattedArg;
        });
        super.log(...formatted);
    }
}
//# sourceMappingURL=sfHelp.js.map