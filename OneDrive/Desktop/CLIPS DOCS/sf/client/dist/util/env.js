/*
 * Copyright (c) 2022, salesforce.com, inc.
 * All rights reserved.
 * Licensed under the BSD 3-Clause license.
 * For full license text, see LICENSE.txt file in the repo root or https://opensource.org/licenses/BSD-3-Clause
 */
import { EnvVars } from '@salesforce/core/envVars';
export class Env extends EnvVars {
    constructor(env = process.env) {
        super(env);
    }
    isAutoupdateDisabled() {
        return this.getBoolean(Env.SF_AUTOUPDATE_DISABLE) || this.getBoolean(Env.SF_DISABLE_AUTOUPDATE);
    }
    isAutoupdateDisabledSet() {
        return !!this.getString(Env.SF_AUTOUPDATE_DISABLE) || !!this.getString(Env.SF_DISABLE_AUTOUPDATE);
    }
    setAutoupdateDisabled(value, updateInstructions) {
        this.setBoolean(Env.SF_AUTOUPDATE_DISABLE, value);
        this.setBoolean(Env.SF_DISABLE_AUTOUPDATE, value);
        if (updateInstructions) {
            this.setUpdateInstructions(updateInstructions);
        }
    }
    setUpdateInstructions(value) {
        this.setString(Env.SF_UPDATE_INSTRUCTIONS, value);
    }
    isDemoMode() {
        return (this.getString(Env.SF_ENV, 'production') || '').toLowerCase() === 'demo';
    }
    isInstaller() {
        return this.getBoolean(Env.SF_INSTALLER);
    }
    normalizeAutoupdateDisabled() {
        // Ensure that the legacy envvar always causes the oclif counterpart to be set
        // see https://github.com/oclif/plugin-update/blob/3946fb296a0a95544ab6364b36a1f7422c8aeddf/src/hooks/init.ts#L22
        if (this.getBoolean(Env.SF_AUTOUPDATE_DISABLE)) {
            this.setBoolean(Env.SF_DISABLE_AUTOUPDATE, true);
        }
        else if (this.getBoolean(Env.SF_DISABLE_AUTOUPDATE)) {
            this.setBoolean(Env.SF_AUTOUPDATE_DISABLE, true);
        }
    }
}
Env.SF_AUTOUPDATE_DISABLE = 'SF_AUTOUPDATE_DISABLE';
Env.SF_DISABLE_AUTOUPDATE = 'SF_DISABLE_AUTOUPDATE';
Env.SF_ENV = 'SF_ENV';
Env.SF_INSTALLER = 'SF_INSTALLER';
Env.SF_NPM_REGISTRY = 'SF_NPM_REGISTRY';
Env.SF_UPDATE_INSTRUCTIONS = 'SF_UPDATE_INSTRUCTIONS';
export default new Env();
//# sourceMappingURL=env.js.map