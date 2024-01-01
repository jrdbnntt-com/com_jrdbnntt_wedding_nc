const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');
const glob = require('glob');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");

const dirs = {
    project: __dirname,
    src: path.resolve(__dirname, './website/src/'),
    output: path.resolve(__dirname, './website/static/build/'),
    node_modules: path.resolve(__dirname, './node_modules/')
}

module.exports = (env, argv) => {
    return {
        devtool: "source-map",
        target: "web",
        context: dirs.src,
        entry: Object.assign(
            {
                main: {
                    import: path.resolve(dirs.src, 'views/_templates/main/index.js')
                }
            },
            collectViewEntries({
                dependOn: [
                    'main',
                ]
            })
        ),
        resolve: {
            modules: [
                __dirname,
                'node_modules'
            ]
        },
        output: {
            path: dirs.output,
            filename: "js/[name].[contenthash].js",
            publicPath: "/static/"
        },
        optimization: {
            minimize: argv.mode !== 'development',
            minimizer: [
                '...',
                new CssMinimizerPlugin(),
            ],
            splitChunks: {
                chunks: 'async',
                minSize: 20000,
                minRemainingSize: 0,
                minChunks: 1,
                maxAsyncRequests: 30,
                maxInitialRequests: 30,
                enforceSizeThreshold: 50000,
                cacheGroups: {
                    node_modules: {
                        test: /[\\/]node_modules[\\/]/,
                        priority: -10,
                        reuseExistingChunk: true,
                        name(module, chunks, cacheGroupKey) {
                            const localNodeModulesDir = 'com_jrdbnntt_wedding_nc/node_modules/'
                            const moduleFilePath = module.identifier();
                            let localNodePath = moduleFilePath.substring(moduleFilePath.lastIndexOf(localNodeModulesDir) + localNodeModulesDir.length);
                            if (localNodePath.includes('|')) {
                                localNodePath = localNodePath
                                    .split('/')
                                    .map((pathPart) => {
                                        if (pathPart.includes('|')) {
                                            return pathPart.substring(0, pathPart.indexOf('|'));
                                        } else {
                                            return pathPart;
                                        }
                                    })
                                    .join('/');
                            }
                            return `${cacheGroupKey}/${localNodePath}`;
                        },
                        chunks: 'all',
                    },
                    default: {
                        minChunks: 2,
                        priority: -20,
                        reuseExistingChunk: true
                    },
                }
            },
        },
        module: {
            rules: [

                // JS
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

                // Sass -> CSS
                {
                    test: /\.s[ac]ss$/i,
                    use: [
                        // Load CSS
                        (argv.mode === 'production' ? MiniCssExtractPlugin.loader : "style-loader"),

                        // Translates CSS into CommonJS
                        "css-loader",


                        // Resolves local url() calls to output paths
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
                },

                // CSS
                {
                    test: /\.css$/i,
                    use: [
                        // Load CSS
                        (argv.mode === 'production' ? MiniCssExtractPlugin.loader : "style-loader"),

                        // Translates CSS into CommonJS
                        "css-loader",
                    ],
                },

                // Load fonts
                {
                    test: /(\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?)|(\.ttf)$/i,
                    type: 'asset/resource',
                    generator: {
                        filename: 'fonts/[name].[contenthash][ext]'
                    }
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
            new MiniCssExtractPlugin({
                filename: 'css/[name].[contenthash].css'
            })
        ]
    }
}

/**
 * Collect all view indexes and name them based on path
 * Entry names are the path from the src folder, with slashes replaced with underscores
 */
function collectViewEntries(entryObjDefaults) {
    let entryMap = {};
    let entryFiles = glob.sync(dirs.src + "/views/**/index.js")
    entryFiles.sort();
    entryFiles.forEach((filePath) => {
        filePath = filePath.substring(dirs.src.length + 1);
        if (!filePath.startsWith("views/_templates/")) {
            let entryKey = "entry_" + filePath.substring(0, filePath.lastIndexOf("/index.js"))
                .split("/")
                .join("_");
            entryMap[entryKey] = Object.assign({
                import: "./" + filePath
            }, entryObjDefaults);
        }
    })
    return entryMap;
}