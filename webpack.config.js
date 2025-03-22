const path = require('path');
const TerserPlugin = require('terser-webpack-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');

const isProduction = process.env.NODE_ENV === 'production';

module.exports = {
	mode: isProduction ? 'production' : 'development',
	entry: './apps/portal/assets/app.js',
	output: {
		path: path.resolve(__dirname, 'apps', 'portal', 'static'),
		publicPath: '/',
		filename: 'portal.min.js',
	},
	resolve: {
		extensions: ['.js', '.jsx'],
	},
	devServer: {
		open: true,
		host: 'localhost',
		hot: true,
	},
	module: {
		rules: [
			{
				test: /\.(js|jsx)$/i,
				exclude: /node_modules/,
				use: {
					loader: 'babel-loader',
					options: {
						presets: ['@babel/preset-env'],
					},
				},
			},
			{
				test: /\.scss$/,
				use: [
					// Always use style-loader so CSS is embedded into the JS bundle
					'style-loader',
					{
						loader: 'css-loader',
						options: {
							importLoaders: 2,
						},
					},
					{
						loader: 'postcss-loader',
						options: {
							postcssOptions: {
								plugins: [
									require('autoprefixer'),
								],
							},
						},
					},
					'sass-loader',
				],
			},
		],
	},
	optimization: {
		minimize: isProduction,
		minimizer: [
			new TerserPlugin({
				terserOptions: {
					compress: {
						drop_console: true, // Optional: Remove console logs in production
					},
				},
			}),
		],
	},
	plugins: [
		// Cleans output directory before each build
		new CleanWebpackPlugin(),
		new CopyWebpackPlugin({
			patterns: [
				{
					from: path.resolve(__dirname, 'apps', 'portal', 'assets', 'favicon.ico'),
					to: path.resolve(__dirname, 'apps', 'portal', 'static', 'favicon.ico'),
				},
			],
		}),
	],
};
