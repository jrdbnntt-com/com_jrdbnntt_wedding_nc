const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const glob = require('glob');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");

const dirs = {
    project: __dirname,
    src: path.resolve(__dirname, './website/src/'),
    output: path.resolve(__dirname, './website/static/build/')
}

module.exports = {
    devtool: "source-map",
    target: "web",
    context: dirs.src,
    entry: collectViewEntries(),
    output: {
        path: dirs.output,
        filename: "[name]-[hash].js"
    },
    optimization: {
        minimize: true,
        minimizer: [
            '...',
            new CssMinimizerPlugin(),
        ]
    },
    module: {
        rules: [
            {
                test: /\.m?jsx?$/,
                exclude: /(node_modules)/,
                use: [
                    // Uses Babel to convert future ES6 features to ES5 code so that it can be used in current browsers
                    {
                        loader: 'babel-loader',
                        options: {
                            presets: [
                                '@babel/preset-env'
                            ],
                            sourceMaps: true,
                            minified: true
                        }
                    }
                ]
            },
            {
                test: /\.s[ac]ss$/i,
                use: [
                    // // Creates `style` nodes from JS strings
                    // "style-loader",

                    // Minify CSS
                    MiniCssExtractPlugin.loader,

                    // Translates CSS into CommonJS
                    "css-loader",

                    // Resolves local url() calls to output paths
                    "resolve-url-loader",
                    {
                        loader: "resolve-url-loader",
                        options: {
                            sourceMap: true
                        }
                    },

                    // Processes CSS with PostCSS
                    {
                        loader: "postcss-loader",
                        options: {
                            postcssOptions: {
                                plugins: [
                                    // Automatically adds vendor prefixes based on Can I Use
                                    "autoprefixer"
                                ]
                            }
                        }
                    },

                    // Compiles Sass to CSS
                    {
                        loader: 'sass-loader',
                        options: {
                            sourceMap: true
                        }
                    }
                ],
            }
        ]
    },
    plugins: [
        new BundleTracker({
            path: dirs.output,
            filename: './webpack-stats.json',
            relativePath: true,
            indent: 2
        }),
        new MiniCssExtractPlugin()
    ]
}

/**
 * Collect all view indexes and name them based on path
 * Entry names are the path from the src folder, with slashes replaced with underscores
 */
function collectViewEntries() {
    let entryMap = {};
    let entryFiles = glob.sync(dirs.src + "/views/**/index.js")
    entryFiles.sort();
    entryFiles.forEach((filePath) => {
        filePath = filePath.substring(dirs.src.length + 1);
        if (!filePath.startsWith("_templates/")) {
            let entryKey = "entry_" + filePath.substring(0, filePath.lastIndexOf("/index.js"))
                .split("/")
                .join("_");
            entryMap[entryKey] = "./" + filePath;
        }
    })
    return entryMap;
}