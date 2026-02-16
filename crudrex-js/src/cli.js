#!/usr/bin/env node

/**
 * CRUDREX CLI - Command Line Interface for Mock JSON Server
 * 
 * @author TraxDinosaur (JavaScript Port)
 * @version 0.1.2
 */

const { Command } = require('commander');
const path = require('path');
const open = require('open');
const MockServer = require('./server');

// Parse command line arguments
const program = new Command();

program
    .name('crudrex')
    .description('Crudrex - Mock JSON Server for Testing HTTP Requests')
    .version('0.1.2')
    .option('-p, --port <number>', 'Port to run the server on', parseInt, 8085)
    .option('-d, --data-dir <path>', 'Directory to store data files', 'data')
    .option('-H, --host <host>', 'Host to run the server on', 'localhost')
    .option('--no-browser', 'Do not open browser automatically')
    .option('-s, --silent', 'Run in silent mode (no startup messages)')
    .parse(process.argv);

const options = program.opts();

// Resolve data directory path
const dataDir = path.resolve(options.dataDir);

// Create and start the server
async function main() {
    try {
        const server = new MockServer({
            dataDir: dataDir,
            port: options.port
        });
        
        // Start the server
        await server.run(options.host, options.silent);
        
        if (!options.silent) {
            console.log('\n CRUDREX - Mock JSON Server');
            console.log('='.repeat(40));
            console.log(`  Server:   http://${options.host}:${options.port}`);
            console.log(`  Data Dir: ${dataDir}`);
            console.log('='.repeat(40));
            console.log('\n  Press Ctrl+C to stop the server\n');
        }
        
        // Open browser if not disabled
        if (options.browser && !options.silent) {
            setTimeout(() => {
                open(`http://${options.host}:${options.port}`);
            }, 1000);
        }
        
        // Handle graceful shutdown
        process.on('SIGINT', () => {
            if (!options.silent) {
                console.log('\n\n  Server stopped. Goodbye!\n');
            }
            server.stop();
            process.exit(0);
        });
        
        process.on('SIGTERM', () => {
            server.stop();
            process.exit(0);
        });
        
    } catch (error) {
        console.error('Error starting server:', error.message);
        process.exit(1);
    }
}

// Run the main function
main();
