<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <h1>Google Drive Encrypted File Rescuer</h1>
    <p>
        This Python script rescues <strong>encrypted files</strong> in Google Drive by downloading older file versions. 
        Specifically, it targets files that were encrypted with a <code>.C85ACF099A00</code> extension (or similar). 
        It recursively scans folders and restores the files by removing the virus-infected extension.
    </p>
    <h2>Features</h2>
    <ul>
        <li><strong>Selective Rescue:</strong> Only rescues files with the <code>.C85ACF099A00</code> extension.</li>
        <li><strong>Folder Traversal:</strong> Recursively processes a folder and its subfolders.</li>
        <li><strong>Preserve File History:</strong> Restores the most recent unencrypted version of a file.</li>
        <li><strong>Automatic Upload:</strong> Uploads the rescued file back to the same folder in Google Drive.</li>
        <li><strong>Prevents Duplicate Work:</strong> Skips already restored files.</li>
    </ul>
    <h2>Requirements</h2>
    <ul>
        <li>Python 3.x</li>
        <li><code>google-api-python-client</code></li>
        <li><code>google-auth</code> and <code>google-auth-oauthlib</code></li>
        <li><code>pytz</code></li>
    </ul>
    <h2>Setup Instructions</h2>
    <ol>
        <li><strong>Clone this repository:</strong>
            <pre><code>git clone https://github.com/YOUR_USERNAME/google-drive-file-rescuer.git
cd google-drive-file-rescuer</code></pre>
        </li>
        <li><strong>Install dependencies:</strong>
            <pre><code>pip install --upgrade google-api-python-client google-auth google-auth-oauthlib pytz</code></pre>
        </li>
        <li><strong>Create a Google Cloud project:</strong>
            <ul>
                <li>Go to <a href="https://console.cloud.google.com/">Google Cloud Console</a>.</li>
                <li>Enable the <strong>Google Drive API</strong> for your project.</li>
                <li>Create OAuth credentials:
                    <ol>
                        <li>Select <strong>Create Credentials &gt; OAuth client ID</strong>.</li>
                        <li>Configure the consent screen and download the <code>credentials.json</code> file.</li>
                    </ol>
                </li>
                <li>Place the downloaded <code>credentials.json</code> in the same folder as the script.</li>
            </ul>
        </li>
        <li><strong>Authenticate the script:</strong>
            <p>On the first run, the script will generate a <code>token.json</code> file after authenticating via your browser. 
            This token stores your access credentials.</p>
        </li>
    </ol>
    <h2>Usage</h2>
    <ol>
        <li><strong>Modify the script:</strong>
            <p>Update the <code>folder_id</code> and <code>target_date</code> in the <code>main()</code> function:</p>
            <pre><code>folder_id = 'YOUR_FOLDER_ID_HERE'  # Replace with the target folder's ID
target_date = '2023-10-01'         # Set the date to fetch previous versions from</code></pre>
            <p>You can get the folder ID from the URL when browsing Google Drive:</p>
            <pre><code>https://drive.google.com/drive/folders/&lt;FOLDER_ID&gt;</code></pre>
        </li>
        <li><strong>Run the script:</strong>
            <pre><code>python google_drive_recovery.py</code></pre>
        </li>
        <li><strong>Expected Output:</strong>
            <pre><code>Entering folder: Important Documents
Processing encrypted file: report.docx.C85ACF099A00
Downloading temp_report.docx
Downloaded temp_report.docx successfully.
Uploaded file 'report.docx' with ID: 123abc456def
Skipping file: summary.pdf (Already rescued or not encrypted)</code></pre>
        </li>
    </ol>
    <h2>License</h2>
    <p>This project is licensed under the MIT License - see the <a href="LICENSE">LICENSE</a> file for details.</p>
    <h2>Disclaimer</h2>
    <p>
        This script provides a method to restore encrypted files but may not recover all files successfully 
        depending on the availability of older versions. Always ensure your Drive is backed up regularly.
    </p>
    <h2>Contributing</h2>
    <p>Contributions are welcome! Feel free to fork this repository and submit pull requests.</p>
    <h2>Acknowledgments</h2>
    <p>Thanks to the Google API and the Python community for making this project possible. 🚀</p>
</body>
</html>
