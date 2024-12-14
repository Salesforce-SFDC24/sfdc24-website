"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.serializeCSVStream = exports.parseCSVStream = exports.toCSV = exports.parseCSV = void 0;
const csv_parse_1 = require("csv-parse");
const sync_1 = require("csv-parse/sync");
const csv_stringify_1 = require("csv-stringify");
const sync_2 = require("csv-stringify/sync");
/**
 * @private
 */
function parseCSV(str, options) {
    return (0, sync_1.parse)(str, { ...options, columns: true });
}
exports.parseCSV = parseCSV;
/**
 * @private
 */
function toCSV(records, options) {
    return (0, sync_2.stringify)(records, { ...options, header: true });
}
exports.toCSV = toCSV;
/**
 * @private
 */
function parseCSVStream(options) {
    return new csv_parse_1.Parser({ ...options, columns: true });
}
exports.parseCSVStream = parseCSVStream;
/**
 * @private
 */
function serializeCSVStream(options) {
    return (0, csv_stringify_1.stringify)({ ...options, header: true });
}
exports.serializeCSVStream = serializeCSVStream;
