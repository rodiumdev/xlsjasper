package bceao.application.bean.business.report.sfm.models;

import lombok.Getter;
import lombok.Setter;
import bceao.commun.service.interfaces.edition.IBeansParams;

@Getter
@Setter
public class SfmRequestParameters implements IBeansParams {
	
	private String ext;
	// [todo] add other request parameters if necessary

	@Override
	public String getExt() {
		return this.ext;
	}

	@Override
	public void SetExt(String ext) {
		this.ext = ext;
	}

}
