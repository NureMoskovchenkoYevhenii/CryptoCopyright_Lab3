// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CopyrightRegistry {

    struct DigitalContent {
        uint256 id;
        string ipfsHash;
        string pHash;
        address author;
        uint256 timestamp;
    }

    DigitalContent[] public allContent;

    mapping(string => bool) private pHashExists;

    event ContentRegistered(uint256 indexed id, string indexed pHash, address indexed author);

    constructor() {
    }

    function registerContent(string memory _ipfsHash, string memory _pHash) public {
        require(!pHashExists[_pHash], "Error: This content (pHash) is already registered!");

        uint256 newId = allContent.length;

        allContent.push(DigitalContent({
            id: newId,
            ipfsHash: _ipfsHash,
            pHash: _pHash,
            author: msg.sender,
            timestamp: block.timestamp
        }));

        pHashExists[_pHash] = true;

        emit ContentRegistered(newId, _pHash, msg.sender);
    }

    function getContentDetails(uint256 _id)
        public
        view
        returns (string memory ipfsHash, string memory pHash, address author, uint256 timestamp)
    {
        require(_id < allContent.length, "Error: Content ID does not exist!");
        DigitalContent storage content = allContent[_id];
        return (content.ipfsHash, content.pHash, content.author, content.timestamp);
    }

    function isPHashRegistered(string memory _pHash) public view returns (bool) {
        return pHashExists[_pHash];
    }

    function getTotalContentCount() public view returns (uint256) {
        return allContent.length;
    }
}
