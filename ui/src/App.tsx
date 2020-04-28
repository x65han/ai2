import React from 'react';
import Popup from 'reactjs-popup';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import LoadMoreButton from './components/LoadMoreButton';

interface Packet {
    distance: string,
    uid: string,
    url: string,
    title: string,
    refURL: string,
}

interface Props { }

interface State {
    fetching: boolean,
    packets: Array<Packet>,
    pageNumber: number,
    srcDoc: string,
}

class App extends React.Component<Props, State> {
    state: State = {
        fetching: true,
        packets: [],
        pageNumber: 1,
        srcDoc: '',
    };

    getReferenceURL(): string {
        const { protocol, host } = window.location;
        return protocol + '//' + host;
    }

    private getBaseURL(pageNumber: number = 1): string {
        const { pathname, protocol, host } = window.location;
        let path = pathname.slice(1);
        if (path.length == 0) {
            path = this.state.srcDoc;
        }
        const QUERY = '?pageNumber=' + pageNumber;
        const BASE = protocol + '//' + host + '/gen/' + path;
        // const BASE = 'http://tuna.cs.uwaterloo.ca:1234/gen/' + path;
        const URL = BASE + QUERY;
        console.log(URL);
        return URL;
    }

    componentDidMount() {
        const URL = this.getBaseURL();
        this.fetchData(URL);
    }

    fetchData(URL: string): void {
        fetch(URL)
            .then(_ => _.json())
            .then(res => {
                console.log(res);
                const { sample, srcDoc } = res;
                this.setState({ fetching: false, packets: sample, srcDoc });
            })
            .catch(e => {
                console.log(e);
                this.setState({ fetching: false });
            });
    }

    loadMore() {
        const URL = this.getBaseURL(this.state.pageNumber + 1);
        this.setState(({ pageNumber }) => ({ pageNumber: pageNumber + 1 }));

        this.fetchData(URL);
    }

    render() {
        const { fetching, packets } = this.state;

        if (fetching === true) {
            return null;
        }

        return (
            <div style={{ margin: '100px' }}>
                <table >
                    <tr>
                        <th>Distance</th>
                        <th>Title</th>
                        <th>Paper URL</th>
                        <th>Use as Source</th>
                    </tr>
                    {
                        packets.map(packet => (
                            <tr key={packet.uid}>
                                <th>{packet.distance}</th>
                                <th>{packet.title}</th>
                                <th>
                                    <a target="__blank" href={packet.url}>View Paper</a>
                                </th>
                                <th>
                                    <a target="__blank" href={packet.refURL}>More...</a>
                                </th>

                            </tr>
                        ))
                    }
                </table>
                <LoadMoreButton onAction={() => this.loadMore()} />
            </div >
        );
    }
}

export default App;
