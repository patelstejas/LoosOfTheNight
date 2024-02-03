// api/process-upload.js
const { parse } = require('url');
const { createReadStream, createWriteStream } = require('fs');
const { pipeline } = require('stream');
const { promisify } = require('util');
const { exec } = require('child_process');
const path = require('path');
const fs = require('fs').promises;

const pipelineAsync = promisify(pipeline);

module.exports = async (req, res) => {
  try {
    const { query } = parse(req.url, true);

    if (!req.headers['content-type'].includes('multipart/form-data')) {
      return res.status(400).json({ error: 'Invalid content type. Must be multipart/form-data.' });
    }

    const imageStream = req.pipe(createWriteStream(`/tmp/${query.imageName}`));

    await pipelineAsync(imageStream, fs.createWriteStream(`/tmp/${query.imageName}`));

    // Execute the Python script
    const pythonProcess = exec(
      `python3 ${path.join(__dirname, 'process-image.py')} ${query.imageName} "${query.location}"`,
      (error, stdout, stderr) => {
        if (error) {
          console.error(`Error: ${error.message}`);
          return res.status(500).json({ error: 'Internal server error.' });
        }

        console.log(`stdout: ${stdout}`);
        console.error(`stderr: ${stderr}`);

        // Respond with the processed data or any other information
        return res.status(200).json({ message: 'Processing complete.' });
      }
    );
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal server error.' });
  }
};
