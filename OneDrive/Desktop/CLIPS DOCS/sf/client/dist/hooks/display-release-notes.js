import ux from '@oclif/core/ux';
export const hook = async function ({ config }) {
    if (process.env.SF_HIDE_RELEASE_NOTES === 'true')
        return;
    try {
        return await config.runCommand('whatsnew', ['--hook']);
    }
    catch (err) {
        const error = err;
        ux.stdout('NOTE: This error can be ignored in CI and may be silenced in the future');
        ux.stdout('- Set the SF_HIDE_RELEASE_NOTES env var to "true" to skip this script\n');
        ux.stdout(error.message);
    }
};
export default hook;
//# sourceMappingURL=display-release-notes.js.map